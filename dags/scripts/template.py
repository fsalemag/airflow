import datetime as dt

template = """Dear {From},
This is an automatic message to the request '{request}' sent on {date} at {time}.

{body}

Best regards,
Francisco's robot
"""

def helpCall(body, commands):
    """Displays available commands and usage"""

    for command in commands:
        body += f"{command}: {commands[command].__doc__}\n"
    
    return body

def weatherCall(body, commands):
    """Gets the current weather"""
    return body

COMMANDS = {
    "help": helpCall,
    "weather": weatherCall
}

def composeMessage(From, To, subject, date):
    # From format: Name <email>, sometimes there is no name
    name, email = From.split("<")
    name = email if len(name) < 4 else name
    email.replace(">", "")

    strTime = date.strftime("%H:%M:%S")
    strDate = date.strftime("%d/%m/%Y")


    # subject is in the form "-e command1 command2 command3"
    commands = subject.split()[1:]

    body = ""

    for command in commands:
        if command in COMMANDS:
            body = COMMANDS[command](body, COMMANDS)
        else:
            body += f"Don't recognize command '{command}'"
    
    msg = template.format(From=name, request=", ".join(commands), body=body, date=strDate, time=strTime)
    return msg, email

if __name__ == "__main__":
    import sendEmail