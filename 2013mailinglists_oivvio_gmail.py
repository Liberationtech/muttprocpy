"""
This is small example of how to use libmuttproc
"""

from libmuttproc import *
from os import environ
home = environ['HOME']


#include this file from your .muttrc
muttfile = open(os.path.join(home, '.mutt/autogenerated_oivvio_gmail'), 'w')

#include this file from your procmailrc
procmailfile = open(
    os.path.join(home, '.procmail/autogenerated_oivvio_gmail'), 'w')


#print warnings to this file
warningsfile = sys.stdout

#your default signature
signaturefile = os.path.join(home, ".signature_mylists")

#your default fromadress
#fromaddress = "Oivvio Polite <oivvio@gmail.com>"
fromaddress = "Oivvio Polite <oivvioslistor@polite.se>"

active = 1
subscribed = 1
printwarnings = 1

#set the defaults for all your mailinglists
all = MailingLists(muttfile, procmailfile, warningsfile,
                   active, subscribed, printwarnings,
                   signaturefile, fromaddress)


#define some lists

MailingList("agile@list.agilesweden.org",
            "/home/oivvio/mail/agile-sweden/",
            "List-Id: Agile Swedens maillista <agile.list.agilesweden.org>", all)

MailingList("exakt@lists.frobbit.se",
            "/home/oivvio/mail/exakt/",
            "List-Id: Exakt IT <exakt.lists.frobbit.se>", all)

#do all the work
all.run()
