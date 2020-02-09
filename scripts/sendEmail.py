import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from airflow.models import Variable

def sendEmail(name, email):
    message = f'Dear {name},\nThis is an automatic message.\n\nWith love,\nFrancisco\'s robot '
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()

    cEmail = Variable.get("hotmail")

    MY_ADDRESS, PASS = cEmail
    s.login(MY_ADDRESS, PASS)

    msg = MIMEMultipart() 

    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=email
    msg['Subject']="This is TEST"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
