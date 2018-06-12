#!/usr/bin/env python

import re
import email
import mailbox
from imaplib import *

MAIL_SERVER = ''
MAILBOX_USER = ''
MAILBOX_PASSWD = ''
MAILBOX_DIR = 'Inbox'
MBOX_OUTFILE = ''

def main(server):
    out_file = mailbox.mbox(MBOX_OUTFILE)
    resp_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
    mboxes = server.list()[1]
    for mbox in mboxes:
        flags, delimiter, mbox_name = resp_pattern.match(mbox).groups()
	#print 'Mailbox name: %s' % mbox_name
	if mbox_name.rfind('INBOX/manual_spam') >= 0:
	    print 'Fetching mail from : %s' % mbox_name
            get_mail(server,mbox_name,out_file)
	#if mbox_name.rfind('Inbox/Sent') >= 0:
	#    print mbox_name
        #    get_mail(server,mbox_name,out_file)
	#get_mail(server,mbox_name,out_file)
    out_file.close()

def get_mail(server,mbox,out_file):
    server.select(mbox, readonly=True)
    typ, data = server.search(None, 'ALL')
    out_file.lock()
    for num in data[0].split():
        res_typ, res_data  = server.fetch(num, '(RFC822)')
	#mail_header = (server.fetch(num,'(BODY[HEADER])')[1][0])[1]
	for response_part in res_data:
	    if isinstance(response_part, tuple):
                response_data = email.message_from_string(response_part[1])
	out_file.add(response_data)
    out_file.flush()
    out_file.unlock()

if __name__ == '__main__':
    server = IMAP4_SSL(MAIL_SERVER)
    server.login(MAILBOX_USER,MAILBOX_PASSWD)
    main(server)
    server.logout()

