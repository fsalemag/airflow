import base64
import datetime as dt
import imaplib
import pprint
import re
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from airflow.models import Variable


# Parses list of tree structure
def parse_list_response(line):
    list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)

# Gets tree structure of email folders
def getStructure(socket, readonly=True):
    typ, data = socket.list()

    # flags, delimiter, mailbox_name = parse_list_response(line.decode('utf-8'))
    return list(map(str.upper, [parse_list_response(line.decode('utf-8'))[2] for line in data]))

# Parses selected messages
def parseMessages(socket, folder, Subject="", From=""):
    typ, data = socket.select(folder.upper(), readonly=False)
    typ, msg_ids = socket.search(None, f'(SUBJECT "{Subject}" FROM "{From}") UNSEEN')

    # Patterns to find in header of email
    pFrom  = r'From: (.*)\r\n'
    pTo = r'To: (.*)\r\n'
    pSubject = r'Subject: ([^\r\n]*).*'
    pDate = r'Date: ([^\r\n]*)'

    for ID in msg_ids[0].split():
        typ, msg_data = socket.fetch(str(int(ID)), '(BODY.PEEK[HEADER])')
        for response_part in msg_data:
            
            if isinstance(response_part, tuple):
                s = response_part[1].decode()    

                if re.search(pSubject, s):                    
                    date = re.search(pDate, s).groups()[0]
                    date = dt.datetime.strptime(date.split(" +")[0], "%a, %d %b %Y %X")

                    subject = re.search(pSubject, s).groups()[0]
                    To = re.search(pTo, s).groups()[0]
                    From = re.search(pFrom, s).groups()[0]

                    if subject.startswith('-e'):
                        socket.store(ID,'+FLAGS','\Seen')
                        return From, To, subject, date
    

def checkInbox(**kwargs):
    try:
        cEmail = Variable.get("hotmail", deserialize_json=True)
        MY_ADDRESS, PASS = cEmail["username"], cEmail["password"]

        M = imaplib.IMAP4_SSL('imap-mail.outlook.com', 993)
        M.login(MY_ADDRESS, PASS) 
        structure = getStructure(M)

        res = parseMessages(M, "Inbox", From="", Subject="")

    except:
        res = None
    finally:
        M.close()
        M.logout()
        return res
