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
from MTLS_Controller import MTLS_Controller
import subprocess
import os

class Talon:
    ServerCommands()
    SubCommands()
    current_command = ""
    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    
    def __init__(self) -> None:
        pass


    def sub_command_handler(self, command: str) -> None:
        if command in SubCommands.subcmds[self.current_command]:
            SubCommands.subcmds[self.current_command][command]["Location"]()
        else:
            self.input_handler(command)
    
    def input_handler(self, user_input: str) -> None:
        parts = user_input.split(maxsplit=1)
        command = parts[0]


        if len(parts) > 1:
            args = parts[1]
        else:
            args = ""
        
        if command == "exit":
            print(self.success +  random.choice(farewells))
            exit()
        elif command == "help":
            ServerCommands.HelperTable.display()
            ServerCommands.AdvancedTable.display()
        elif command == "settings":
            self.current_command = "settings"
        elif command == "crack":
            self.current_command = "crack"
        elif command == "MTLS":
            self.current_command = "MTLS"
        elif command == "back":
            self.current_command = None
        elif command == "show":
            print(args)
            if not args:
                print(self.fail + "Please state what you would like to show")
                return
            if args == "options" and self.current_command:
                self.show_options()
            if args == "connections":
                MTLS_Controller.show_connections()

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
            if self.current_command and command in SubCommands.subcmds[self.current_command]:
                self.sub_command_handler(command)
            else:
                process = subprocess.run(user_input, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if process.returncode == 0:
                    print(process.stdout)
                else:
                    print(self.fail + "Unknown server and bash command")

    def show_options(self):
        print(self.success + self.current_command)
        if not self.current_command or self.current_command not in ServerCommands.SList:
            print(self.fail + "No command selected or no options availabsetle for the current command.")
            return
        table = ServerCommands.SList[self.current_command]["Table"]
        table.display()
        try:
            if SubCommands.subcmds[self.current_command]:
                print(self.success + "Sub Commands:")
                for subcommand in SubCommands.subcmds[self.current_command]:
                    print(" - " + subcommand)
        except:
            return
    def set_option(self, option: str, value: str) -> None:
    
        if self.current_command:
            if option in ServerCommands.SList[self.current_command]["Options"] and value:
                ServerCommands.SList[self.current_command]["Options"][option]["Value"] = value
                ServerCommands.SList[self.current_command]["Table"].modify_row(ServerCommands.SList[self.current_command]["Options"][option]["Location"] , value)
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
    
   
    username = ServerCommands.SList["settings"]["Options"]["Username"]["Value"]
 
    Talon = Talon()
    print(Banner)
    session = PromptSession(history=InMemoryHistory())
    try:
        while True:
            if Talon.current_command:
               
                prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> <ansiwhite>[</ansiwhite><ansired>{command}</ansired><ansiwhite>] > </ansiwhite>'.format(username=username, ip=ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"], command=Talon.current_command))
            else:
                prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> '.format(username=ServerCommands.SList["settings"]["Options"]["Username"]["Value"], ip=ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"]))
            # Use prompt_toolkit's session to read input with support for history
            
            user_input = session.prompt(prompt_text)
            Talon.input_handler(user_input)
    except KeyboardInterrupt:
        print(Talon.success + random.choice(farewells))

        exit()
