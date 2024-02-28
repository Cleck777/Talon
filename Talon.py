from typing import Callable, Dict, Optional
#from CommandFactory import CommandFactory
from prompt_toolkit import PromptSession
import random
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text, HTML, ANSI
from server_commands import ServerCommands 
from termcolor import colored
from HelpTable import HelpTable
from OptionsTable import OptionsTable
from Farwells import farewells
from sub_commands import SubCommands
import subprocess
import os

class Talon:
    current_command = ""
    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    server_commands = ServerCommands()
    sub_commands = SubCommands()
    def __init__(self) -> None:
        pass


    def sub_command_handler(self, command: str) -> None:
        if command in self.sub_commands.subcmds[self.current_command]:
            self.sub_commands.subcmds[self.current_command][command]["Location"]()
        else:
            self.input_handler(command)
    
    def input_handler(self, user_input: str) -> None:
        parts = user_input.split(maxsplit=1)
        command = parts[0]


        if len(parts) > 1:
            args = parts[1]
        else:
            args = ""
        try :
            self.sub_command_handler(command)
            return
        except:
            pass
        if command == "exit":
            print(self.success +  random.choice(farewells))
            exit()
        elif command == "help":
            self.server_commands.HelperTable.display()
            self.server_commands.AdvancedTable.display()
        elif command == "settings":
            self.current_command = "settings"
        elif command == "crack":
            self.current_command = "crack"
        elif command == "MTLS":
            self.current_command = "MTLS"
        elif command == "back":
            self.current_command = None
        elif command == "show":
            if not args:
                print(self.fail + "Please state what you would like to show")
                return
            if args == "options" and self.current_command:
                self.show_options()
            else: 
                print(self.fail + "No command selected")
        elif command == "set":
            if not args:
                print(self.fail + "Please state what you would like to set")
                return
            if self.current_command:
                option, value = args.split(maxsplit=1)
                self.set_option(option, value)
            else:
                print(self.fail + "No command selected")
        
            
        else:
            process = subprocess.run(user_input, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if process.returncode == 0:
                print(process.stdout)
            else:
                print(self.fail + "Unknown server and bash command")

    def show_options(self):
        print(self.success + self.current_command)
        if not self.current_command or self.current_command not in self.server_commands.SList:
            print(self.fail + "No command selected or no options availabsetle for the current command.")
            return
        table = self.server_commands.SList[self.current_command]["Table"]
        table.display()
        try:
            if self.sub_commands.subcmds[self.current_command]:
                print(self.success + "Sub Commands:")
                for subcommand in self.sub_commands.subcmds[self.current_command]:
                    print(" - " + subcommand)
        except:
            return
    def set_option(self, option: str, value: str) -> None:
        if self.current_command:
            if option in self.server_commands.SList[self.current_command]["Options"]:
                ServerCommands.server_commands.SList[self.current_command]["Options"][option]["Value"] = value
                print(self.success + "Set " + option + " to " + value)
            else:
                print(self.fail + "Option not found")
        else:
            print(self.fail + "No command selected")
            


if __name__ == "__main__":
  

    Banner = colored('''┏┳┓┏┓┓ ┏┓┳┓  ┏┓┏┓''', 'green') + '''\n'''
    Banner += colored(''' ┃ ┣┫┃ ┃┃┃┃  ┃ ┏┛''', 'light_green') + '''\n'''
    Banner += colored(''' ┻ ┛┗┗┛┗┛┛┗  ┗┛┗━''', 'light_yellow') + '''\n'''
    Banner += colored('''https://github.com/Cleck777/Talon              v2.0''', 'white') + '''\n'''
    style = Style.from_dict({
    'prompt': '#ff6b6b',  # Using an RGB value for custom color
})
    current_command = Talon.current_command
    server_commands = Talon.server_commands
   
    username = server_commands.SList["settings"]["Options"]["Username"]["Value"]
 
    Talon = Talon()
    print(Banner)
    session = PromptSession(history=InMemoryHistory())
    try:
        while True:
            if Talon.current_command:
               
                prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> <ansiwhite>[</ansiwhite><ansired>{command}</ansired><ansiwhite>] > </ansiwhite>'.format(username=username, ip=server_commands.SList["settings"]["Options"]["Server_IP"]["Value"], command=Talon.current_command))
            else:
                prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> '.format(username=username, ip=server_commands.SList["settings"]["Options"]["Server_IP"]["Value"]))
            # Use prompt_toolkit's session to read input with support for history
            
            user_input = session.prompt(prompt_text)
            Talon.input_handler(user_input)
    except KeyboardInterrupt:
        print(Talon.success + random.choice(farewells))
        exit()
