"""
This is small example of how to use libmuttproc
"""

from libmuttproc import *
from os import environ
home = environ['HOME']


#include this file from your .muttrc
muttfile = open(os.path.join(home, '.mutt/autogenerated_mylists_polite'), 'w')

#include this file from your procmailrc
procmailfile = open(
    os.path.join(home, '.procmail/autogenerated_mylists_polite'), 'w')


#print warnings to this file
warningsfile = sys.stdout

#your default signature
signaturefile = os.path.join(home, ".signature_mylists")

#your default fromadress
fromaddress = "Oivvio Polite <mylists@polite.se>"

active = 1
subscribed = 1
printwarnings = 1

#set the defaults for all your mailinglists
all = MailingLists(muttfile, procmailfile, warningsfile,
                   active, subscribed, printwarnings,
                   signaturefile, fromaddress)


#define some lists

MailingList("tmux-users@lists.sourceforge.net",
            "/home/oivvio/mail/tmux-users/",
            "List-Id: <tmux-users.lists.sourceforge.net>", all)

MailingList("django-users@googlegroups.com",
            "/home/oivvio/mail/django-users/",
            "List-ID: <django-users.googlegroups.com>", all)


MailingList("django-users@googlegroups.com",
            "/home/oivvio/mail/django-users/",
            "List-ID: <django-users.googlegroups.com>", all)


MailingList("vim_use@googlegroups.com",
            "/home/oivvio/mail/vim-use/",
            "List-ID: <vim_use.googlegroups.com>", all)

MailingList("css-d@lists.css-discuss.org",
            "/home/oivvio/mail/css-d/",
            "List-Id: Practical discussions of CSS and its use <css-d.lists.css-discuss.org>", all)


MailingList("phonegap@googlegroups.com",
            "/home/oivvio/mail/phonegap/",
            "List-ID: <phonegap.googlegroups.com>", all)

MailingList("selenium-users@googlegroups.com",
            "/home/oivvio/mail/selenium-users/",
            "List-ID: <selenium-users.googlegroups.com>", all)

MailingList(
    "meteor-talk@googlegroups.com",
    "/home/oivvio/mail/meteor-talk/",
    "List-ID: <meteor-talk.googlegroups.com",
    all)

MailingList(
    "salt-users@googlegroups.com",
    "/home/oivvio/mail/salt-users/",
    "List-ID: <salt-users.googlegroups.com>",
    all)

MailingList(
    "angular@googlegroups.com",
    "/home/oivvio/mail/angular/",
    "List-ID: <angular.googlegroups.com>",
    all)

MailingList(
    "agile@list.agilesweden.com",
    "/home/oivvio/mail/agile-sweden/",
    "List-Id: Agile Swedens maillista <agile.list.agilesweden.com>",
    all)

MailingList(
    "podcasters@yahoogroups.com",
    "/home/oivvio/mail/podcasters/",
    "List-Id: <podcasters.yahoogroups.com>",
    all)

MailingList(
    "podcasters@yahoogroups.com",
    "/home/oivvio/mail/podcasters/",
    "List-Id: <podcasters.yahoogroups.com>",
    all)

MailingList(
    "cmusphinx-devel@lists.sourceforge.net",
    "/home/oivvio/mail/cmusphinx-devel/",
    "List-Id: <cmusphinx-devel.lists.sourceforge.net>",
    all)

#do all the work
all.run()