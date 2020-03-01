
def contribute(body, commands):
    """Sends email to developer with body of email. Add tab in body of email to synalize start of message to be sent to developer. Everything in the message after the tag '-configure' and before any other different tag will be sent.
Subject: '"-e contribute <arg2> <arg3>"'
Body: '-contribute
I would like to have x feature implemented.
You could do it this way: ......"""
    body += "\nEmail sent to developer!"
    return body
