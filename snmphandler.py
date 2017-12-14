#!/usr/bin/env python

"""

 Need to add the below line in snmptrapd.conf
 	'traphandle default /usr/local/sbin/snmphandler.py'
 This will have the snmptrapd daemon to redirect all received trap to the script 
 mentioned, "/usr/local/sbin/snmphandler.py", for processing after logging the same to the 
 system log.

"""


import os 
import re
import sys
import smtplib
import logging as logger

logger.basicConfig(level=logger.DEBUG,
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename='/tmp/snmplog.txt',
            filemode='a')


def main():

    base_dir = os.getcwd()
    value_patt = re.compile("\"(.*?)\"")
    trap_data = []
    orig_data = ''
    for data in sys.stdin.readlines():
        orig_data += data
        if value_patt.findall(data):
            trap_data.append(value_patt.findall(data)[0])

    if len(trap_data) < 4:
        sys.exit()

    body = """
    Remote Host     = %s
    Remote Process  = %s
    Event Type      = %s
    Event Value     = %s
    """ % (trap_data[1],trap_data[0],trap_data[3],trap_data[2])

    body += '\n\noriginal trap msg: %s' % orig_data
    logger.info('Trap received:\n%s' % body)
    mailman(body,trap_data[1])

def mailman(body,remote_host):

    to = [""]
    subject = "SNMP Trap received from %s" % remote_host
    sender = ""
    smtp_server = ""
    smtp_user = ""
    smtp_passwd = ""

    headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, to, subject)
    message = headers + body 

    mailer = smtplib.SMTP(smtp_server)
    mailer.debuglevel = 1
    mailer.login(smtp_user, smtp_passwd)
    smtpresult = mailer.sendmail(sender, to, message)

    if smtpresult:
        errstr = ""
        for recip in smtpresult.keys():
            errstr = """Could not delivery mail to: %s

    Server said: %s
    %s

    %s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr)
        logger.error("Error sending mail: \n%s" % errstr)
        raise smtplib.SMTPException, errstr
   
    mailer.quit()

if __name__ == '__main__':

    main()
