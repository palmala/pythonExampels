import string
from string import Template

if __name__ == "__main__":
    print(string.digits)
    print(string.punctuation)

    # templating
    from string import Template
    cmd_template = Template("assuming I run command $command")
    my_cmd = cmd_template.substitute(command="clear")
    print(my_cmd)
