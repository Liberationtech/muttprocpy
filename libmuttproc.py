"""
libmuttproc - add new mailinglists without editing a thousand configfiles.

This is a little utility for people using the mutt/procmail/maildir
combo. When subscribing to a new mailinglists the user only have to
add ONE line to ONE file. libmuttproc will help you generate procmail
rules, check that maildir folders you specify actually exist, add some
mutt folder-hooks, and other stuff that mutt needs

for an example of how to use libmuttproc see mymailinglists_example.py

other then that the source is the documentation

"""

import os, sys, re

def generate_maildir(maildir):
    os.makedirs(maildir, 0755)
    os.makedirs(os.path.join(maildir, "cur"), 0755)
    os.makedirs(os.path.join(maildir, "new"), 0755)
    os.makedirs(os.path.join(maildir, "tmp"), 0755)

class MailingLists:
    def __init__(self,
                 muttlistsfile,
                 procmailfile,
                 warningsfile,
                 active,
                 subscribed,
                 printwarnings,
                 signaturefile,
                 fromaddress):

        self.__data = []
        self.muttlistsfile = muttlistsfile
        self.procmailfile = procmailfile
        self.warningsfile = warningsfile
        self.active = active
        self.subscribed = subscribed
        self.printwarnings = printwarnings
        self.signaturefile = signaturefile
        self.fromaddress = fromaddress

    def append(self, mailinglist):
        self.__data.append(mailinglist)

        if not mailinglist.__dict__.has_key('active'):
            mailinglist.active = self.active

        if not mailinglist.__dict__.has_key('subscribed'):
            mailinglist.subscribed = self.subscribed

        if not mailinglist.__dict__.has_key('printwarnings'):
            mailinglist.printwarnings = self.printwarnings

        if not mailinglist.__dict__.has_key('signaturefile'):
            mailinglist.signaturefile = self.signaturefile

        if not mailinglist.__dict__.has_key('fromaddress'):
            mailinglist.fromaddress = self.fromaddress

    def __warn(self, msg):
        if self.printwarnings:
            self.warningsfile.write(msg)

    def run(self):
        for mailinglist in self.__data:
            if not mailinglist.maildir_exists():
                self.__warn("Mailbox '%s' does not exist - let me generate that for you \n" % mailinglist.mailbox)
                mailinglist.generate_maildir()

            if not mailinglist.correct_maildir_syntax():
                self.__warn("Mailbox '%s' does not have correct maildir syntax\n" % mailinglist.mailbox)

            if not mailinglist.check_for_files_in_maildir():
                self.__warn("Mailbox '%s' does not contain any messages\n" % mailinglist.mailbox)
            elif not mailinglist.correct_regexp():
                self.__warn("At least one message in mailbox '%s' does not match the procmail regexp\n" % mailinglist.mailbox)



            self.muttlistsfile.write(mailinglist.generate_mutt_config())
            self.procmailfile.write(mailinglist.generate_procmail_rule())


class MailingList:
    def __init__(self, address, mailbox, regexp, mailinglists):
        self.address = address
        self.mailbox = mailbox
        self.regexp = regexp
        self.escape_regexp()
        mailinglists.append(self)

    def maildir_exists(self):
        return os.path.isdir(self.mailbox)

    def generate_maildir(self):
        os.makedirs(self.mailbox, 0755)
        os.makedirs(os.path.join(self.mailbox, "cur"), 0755)
        os.makedirs(os.path.join(self.mailbox, "tmp"), 0755)
        os.makedirs(os.path.join(self.mailbox, "new"), 0755)

    def correct_maildir_syntax(self):
        result = 0
        if self.mailbox[-1:] == "/":
            result = 1
        return result

    def check_for_files_in_maildir(self):
        result = 0
        entries = []

        curdir = os.path.join(self.mailbox,'cur')
        curentries = os.listdir(curdir)
        entries += map(os.path.join, (curdir,) * len(curentries), curentries)

        newdir = os.path.join(self.mailbox,'new')
        newentries = os.listdir(newdir)
        entries += map(os.path.join, (newdir,) * len(newentries), newentries)
        for entry in entries:
            isfile = os.path.isfile(entry)
            if isfile:
                result = entry
                break
        return result

    def correct_regexp(self):
        """
        Locates ONE file in the maildir and checks if it matches the regexp
        """
        result = 0
        procmailregexp = re.compile(self.regexp)
        filename = self.check_for_files_in_maildir()
        if filename:
            file = open(filename,'r')
            for line in file:
                match = procmailregexp.search(line)
                if match:
                    result = 1
                    break
        return result

    def escape_regexp(self):
        #brackets occur in mail headers
        #but they also have regexp significance so we have to escape them

        self.regexp = self.regexp.replace("[","\\[")
        self.regexp = self.regexp.replace("]","\\]")

    def generate_procmail_rule(self):
        return "#autogenerated rule for %s\n:0\n* %s\n%s\n" % (self.address, self.regexp, self.mailbox)

    def generate_mutt_config(self):
        return "%s%s%s%s%s%s%s\n" % (self.generate_mailboxes_line(),
                                 self.generate_lists_line(),
                                 self.generate_subscribe_line(),
                                 self.generate_folder_hook_from(),
                                 self.generate_folder_hook_signature(),
                                 self.generate_folder_hook_to(),
                                 self.generate_folder_hook_color_index()
                                 )


    def generate_mailboxes_line(self):

        if self.active:
            result = "mailboxes %s\n" % self.mailbox
        else:
            result = "#mailboxes %s\n" % self.mailbox
        return result


    def generate_lists_line(self):
        return "lists %s\n" % self.address


    def generate_subscribe_line(self):
        if self.subscribed:
            result = "subscribe %s\n" % self.address
        else:
            result = "#subscribe %s\n" % self.address

        return result

    def generate_from_template(self, template, pair1,pair2):
        result = template
        result = result.replace(pair1[0],pair1[1]);
        result = result.replace(pair2[0],pair2[1]);
        result = result.replace("#", '"');
        result += "\n"
        return result


    def generate_folder_hook_to(self):
        template = 'folder-hook MAILFOLDER #macro index m \#<mail>ADDRESS\##'
        return self.generate_from_template(template,
                                           ("MAILFOLDER", self.mailbox),
                                           ("ADDRESS", self.address))


    def generate_folder_hook_from(self):
        template = 'folder-hook MAILFOLDER my_hdr From: FROMADDRESS'
        return self.generate_from_template(template,
                                           ("MAILFOLDER", self.mailbox),
                                           ("FROMADDRESS", self.fromaddress))


    def generate_folder_hook_signature(self):
        template = 'folder-hook MAILFOLDER  set signature=#SIGNATUREFILE#'
        return self.generate_from_template(template,
                                           ("MAILFOLDER", self.mailbox),
                                           ("SIGNATUREFILE", self.signaturefile))



    def generate_folder_hook_color_index(self):
        template = 'folder-hook MAILFOLDER  \'color index red default #~p|~P#\''
        return self.generate_from_template(template,
                                           ("MAILFOLDER", self.mailbox),
                                           ("MAILFOLDER", self.mailbox))




ML = MailingList
