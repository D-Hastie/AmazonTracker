#!/usr/bin/python

import imaplib
import email
import os
import Mailconf
import directories
svdir = directories.AttachmentLoc
print 'Starting Mail Check'
print 'Begin set up info'
print 'Server setup'
mail=imaplib.IMAP4_SSL(Mailconf.server, 993)

print 'Begin login user'
mail.login(Mailconf.login,Mailconf.pw)

print 'Select Mailbox'
mail.select("Inbox")
print 'Imap stuff begins'

while True:
    imap = imaplib.IMAP4_SSL(Mailconf.server)
    r, d = imap.login(Mailconf.login, Mailconf.pw)
    assert r == 'OK', 'login failed'
    try:
        print 'IMAP re-login done'
    # do things with imap
    except imap.abort, e:
        continue
    imap.logout()
    break

print 'Initial setup complete'
print 'Starting Search'

typ, msgs = mail.search(None, '(SUBJECT "Test")')
msgs = msgs[0].split()

print 'End search'

for emailid in msgs:
    resp, data = mail.fetch(emailid, "(RFC822)")
    email_body = data[0][1] 
    m = email.message_from_string(email_body)
    print 'Found ID'
    if m.get_content_maintype() != 'multipart':
        continue

    for part in m.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename=part.get_filename()
        if filename is not None:
            # file_path = open(svdir+filename, 'a')
            file_path = os.path.join(svdir, filename,)
            print 'File already exists'
            if not os.path.isfile(file_path):
                print 'New file found.'
                print 'Downloaded content to mailattach folder'
                print file_path       
                fp = open(file_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

print 'End mail check and fetch phase.'
print ' '
