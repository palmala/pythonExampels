import string
from string import Template

asd = "Whatever you want to"

mycmd = "assuming I run command $command"

if __name__ == "__main__":
    print(string.digits)
    print(string.punctuation)
    cmd_template = Template(mycmd)
    mycmd = cmd_template.substitute(command="clear")
    print(mycmd)