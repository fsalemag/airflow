import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from airflow.models import Variable
from scripts.template import composeMessage
import datetime

def sendEmail(**kwargs):

    ti = kwargs['ti']
    inbox = ti.xcom_pull(key=None, task_ids='check_inbox')

    if inbox and isinstance(inbox, tuple):
        From, To, subject, date = inbox

        message, email = composeMessage(From, To, subject, date)

        
        s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        s.starttls()

        cEmail = Variable.get("hotmail", deserialize_json=True)
        MY_ADDRESS, PASS = cEmail["username"], cEmail["password"]
        s.login(MY_ADDRESS, PASS)

        msg = MIMEMultipart() 

        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Automatic reply"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)

        print(f"Sent email to '{email}'")
        return "Success"
    else:
        print("Nothing in the mailbox")
        return None
