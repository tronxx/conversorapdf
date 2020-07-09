"""
   Copyright (C) 2014 Javier Montes @montesjmm montesjmm.com
   License: http://opensource.org/licenses/MIT
 
   What does this script do?
 
   All of your emails with a subject like:
   "d>tag_name"
   and with an url in the body, will be saved to delicious.com
 
   In other words, you can save links to delicious simply sending emails
   to yourself!!!! <img class="emoji" draggable="false" alt="??" src="http://s.w.org/images/core/emoji/72x72/1f609.png">
"""
import imaplib
import email
import re
import urllib
import urllib2
from unicodedata import normalize
from email.header import decode_header
from email.header import make_header
import os, sys
 
gmail_username = ''
gmail_password = ''
delicious_username = ''
delicious_password = ''
 
 
def connect_to_gmail(username, password):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(username, password)
    imap.select("inbox")
 
    return imap
 
 
# this function from: http://i2bskn.hateblo.jp/entry/20120322/1332421932
def get_subject(email):
    h = decode_header(email.get('subject'))
    return unicode(make_header(h)).encode('utf-8')
 
 
# this function from: https://gist.github.com/miohtama/5389146
def get_decoded_email_body(message_body):
    """ Decode email body.
    Detect character set if the header is not set.
    We try to get text/plain, but if there is not one then fallback to text/html.
    :param message_body: Raw 7-bit message body input e.g. from imaplib. Double encoded in quoted-printable and latin-1
    :return: Message body as unicode string
    """
 
    msg = email.message_from_string(message_body)
 
    text = ""
    if msg.is_multipart():
        html = None
        for part in msg.get_payload():
 
            #print "%s, %s" % (part.get_content_type(), part.get_content_charset())
 
            if part.get_content_charset() is None:
                # We cannot know the character set, so return decoded "something"
                text = part.get_payload(decode=True)
                continue
 
            charset = part.get_content_charset()
 
            if part.get_content_type() == 'text/plain':
                text = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
 
            if part.get_content_type() == 'text/html':
                html = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
 
        if text is not None:
            return text.strip()
        else:
            return html.strip()
    else:
        text = unicode(msg.get_payload(decode=True), msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
        return text.strip()
 
 
def save_to_delicious(save_url, username, password, tag):
    req = urllib2.Request(save_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36')
    html = urllib2.urlopen(req)
 
    if (html):
        html = html.read()
    if (html):
        match_title = re.match(r'.*?<title>(.*?)</title>', html, re.I | re.M | re.DOTALL)
        title = match_title.group(1)
        title = title.decode('utf-8')
        title = normalize('NFD', unicode(title)).encode('ascii', 'ignore')
        delicious_url = "https://api.del.icio.us/v1/posts/add?&shared=no&url=" + urllib.quote_plus(save_url) + "&tags=" + tag + "&description=" + urllib.quote_plus(title.encode('ascii', 'ignore'))
    else:
        delicious_url = "https://api.del.icio.us/v1/posts/add?&shared=no&url=" + urllib.quote_plus(save_url) + "&tags=" + tag
 
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, delicious_url, username, password)
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))
 
    req = urllib2.Request(delicious_url)
    urllib2.urlopen(req)
 
## --> Comienza Main
micuenta_z      = sys.argv[1]
pwd_z	          = sys.argv[2]
subjectbus_z    = sys.argv[3]
print "Subject Buscado:", subjectbus_z;
 
imap = connect_to_gmail(micuenta_z, pwd_z)
result, mails_data = imap.search(None, "(UNSEEN)")
 
mails_ids = mails_data[0]
mails_id_list = mails_ids.split()
eliminar_z = "NO"

mail_count = 40
for idemail_z in reversed(mails_id_list):
 
    result, mail_data = imap.fetch(idemail_z, "(RFC822)")
    raw_email = mail_data[0][1]
    this_email = email.message_from_string(raw_email)
 
    subject_z = get_subject(this_email)
    print subject_z
 
    if subject_z == subjectbus_z :
        body = "Recibiendo"
        print body
           
        for part in this_email.walk():
        		if part.get_content_maintype() == 'multipart':
        		   continue
        		if part.get('Content-Disposition') is None:
        		   continue
        		filename = part.get_filename()
        		att_path = filename
        		fp = open(att_path, 'wb')
        		fp.write(part.get_payload(decode=True))
        		fp.close()
        #Fin For
        if eliminar_z == "SI":
          imap.copy(idemail_z, '[Gmail]/Trash')
          imap.store(idemail_z, '+FLAGS', r'(\Deleted)')
        else:
          imap.store(idemail_z, '+FLAGS', r'(\Seen)')
        #End if 
        imap.expunge()
    else:
      imap.store(idemail_z, '-FLAGS', r'(\Seen)')
    #Fin If
    if subject_z == subjectbus_z :
       break
    # Si ya encontre el que busco ya no continuo la busqueda

    mail_count -= 1
    if mail_count < 1:
        break
#Fin For