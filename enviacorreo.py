#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os, sys

gmail_user = "tronxx@gmail.com"
gmail_pwd = "kdba2504"

def mail(destino_z, subject, text, remite_z, pwd_z, attach=None):
   msg = MIMEMultipart()
   
   msg['From'] = remite_z
   msg['To'] = destino_z
   msg['Subject'] = subject
            
   msg.attach(MIMEText(text))
   
   for miattach_z in attach:
     part = MIMEBase('application', 'octet-stream')
     part.set_payload(open(miattach_z, 'rb').read())
     Encoders.encode_base64(part)
     part.add_header('Content-Disposition',
         'attachment; filename="%s"' % os.path.basename(miattach_z))
     msg.attach(part)
   #End For
                                         
   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(remite_z, pwd_z)
   mailServer.sendmail(remite_z, destino_z, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

correodest_z = sys.argv[1]
print "Destino ", correodest_z;
subject_z    = sys.argv[2]
print "Subject ", subject_z;
msg_z        = sys.argv[3]
print "msg ", msg_z;
remite_z     = sys.argv[4]
print "remite ", remite_z;
pwd_z	     = sys.argv[5]
print "pwd ", pwd_z;
adjuntos_z   = sys.argv[6]
print "adjuntos ", adjuntos_z;
misadjuntos_z = []

adj_z = open(adjuntos_z, 'r')
for linea_z in adj_z:
    misadjuntos_z.append(linea_z.strip("\n"))
adj_z.close()
print misadjuntos_z
                                                                 
mail(correodest_z,
   subject_z,
   msg_z,
   remite_z,
   pwd_z,
   misadjuntos_z)
