import os
import sys
import smtplib
import random
import requests
from bs4 import BeautifulSoup
# For guessing MIME type based on file name extension
import mimetypes

from optparse import OptionParser

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


path = ''
fromaddr = 'abcd@hocmen.com'
toaddr = 'malware@yeehawjerky.com'

def get_filename():
    filename = random.choice(os.listdir(path))
    print (filename)
    return filename

def sendthemail(fromaddr, frompwd, toaddr, payload):
    server = smtplib.SMTP('mail.hocmen.com', 25)
    server.starttls()
    server.login(fromaddr,frompwd)
    server.sendmail(fromaddr, toaddr, payload)
    server.quit()

def get_pwd():
    get_file = path + 'pwd'
    pwd_file = open(get_file, 'r')
    the_pwd = pwd_file.read()
    return the_pwd.split('\n')[0]

def make_subject_preamble():
    things = BeautifulSoup(requests.get('http://www.sfgate.com').text).find_all('li','mostPopular--list-item')
    subject = str(str(str(random.choice(things)).split('>')[2].split('<')[0]))
    preamble = str(str(str(random.choice(things)).split('>')[2].split('<')[0]))
    print (subject + '\n' + preamble +'\n')
    return subject, preamble

def create_mail():
#    the_file = get_filename()
#    the_file = 'a596deea7c4d0bfc20eeb2cedec3c854'
    the_file = str(sys.argv[1])
    ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/',1)
    whole_file = the_file
    fp = open(whole_file, 'rb')
    msg = MIMEBase(maintype,subtype)
    msg.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(msg)
    msg.add_header('Content-Disposition', 'attachment', filename = the_file)
    outer = MIMEMultipart()
    sub, pre = make_subject_preamble()
    outer['Subject'] = sub
    outer['To'] = toaddr
    outer['From'] = fromaddr
    outer.preamble = pre
    outer.attach(msg)
    payload = outer.as_string()
    return payload

send_pwd = get_pwd()
attachment = create_mail()
sendthemail(fromaddr, send_pwd, toaddr, attachment)
