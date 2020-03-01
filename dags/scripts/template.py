from scripts.contribute import contribute
from scripts.email import template


def helpCall(body, commands):
    """Displays available commands and usage"""

    body += "Welcome to my Pyflow bot. To execute a command send an email to 'pyflow@hotmail.com' with the subject '-e <command>'."
    body += "\nThere can be multiple commands. The currently available commands are:\n"

    for command in commands:
        body += f"{command}: {commands[command].__doc__}\n"
    
    return body


COMMANDS = {
    "help": helpCall,
    "contribute": contribute 
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
    
    body += "\n\n\nProject: github.com/fsalemag/airflow"

    msg = template.format(From=name, request=", ".join(commands), body=body, date=strDate, time=strTime)
    return msg, email

if __name__ == "__main__":
    import sendEmail
