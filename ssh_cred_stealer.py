import MockSSH
import random
import string
from twisted.cred import checkers

# Dirty hack to override default twisted behavior    
class CredsToStdOut(checkers.InMemoryUsernamePasswordDatabaseDontUse):
    def requestAvatarId(self, credentials):
        print("Authentication attempt: %s / %s" % (credentials.username, credentials.password))
        return super(CredsToStdOut, self).requestAvatarId(credentials)

MockSSH.checkers.InMemoryUsernamePasswordDatabaseDontUse = CredsToStdOut

def passwd_change_protocol_prompt(instance):
    instance.protocol.prompt = "hostname #"
    instance.protocol.password_input = False

def passwd_write_password_to_transport(instance):
    instance.writeln("")

command_passwd  =  MockSSH.PromptingCommand(
    name = 'passwd',
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(99)),
    prompt = "Password: ",
    success_callbacks = [passwd_change_protocol_prompt],
    failure_callbacks = [passwd_write_password_to_transport])

users = {'admin': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(99))}
commands = [command_passwd]
MockSSH.runServer(commands, prompt = "hostname>", interface = '0.0.0.0', port = 2222, **users)
