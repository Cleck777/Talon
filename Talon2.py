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
    def __init__(self) -> None:
        self.current_command = ""
        self.success = colored('[+] ', 'green')
        self.fail = colored('[-] ', 'red')
    
    def sub_command_handler(self, command: str) -> None:
        try:
            if command in SubCommands.subcmds.get(self.current_command, {}):
                SubCommands.subcmds[self.current_command][command]["Location"]()
        except KeyError:
            print(self.fail + "Invalid sub-command")
            self.input_handler(command)
    
    def input_handler(self, user_input: str) -> None:
        parts = user_input.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if command == "exit":
            print(self.success + random.choice(farewells))
            exit()
        elif command == "help":
            ServerCommands.HelperTable.display()
            ServerCommands.AdvancedTable.display()
        elif command in ["settings", "crack", "MTLS", "HTTPS"]:
            self.current_command = command
        elif command == "back":
            self.current_command = ""
        elif command == "show":
            self.handle_show_command(args)
        elif command == "set":
            if args:
                self.handle_set_command(args)
            else:
                print(self.fail + "Please state what you would like to set")
        else:
            self.handle_other_commands(command, user_input)

    def handle_show_command(self, args: str):
        if not args:
            print(self.fail + "Please state what you would like to show")
            return
        
        if args == "options" and self.current_command:
            self.show_options()
        elif args == "connections":
            MTLS_Controller.show_connections()
        else: 
            print(self.fail + "No command selected or invalid argument")

    def handle_set_command(self, args: str):
        try:
            option, value = args.split(maxsplit=1)
            self.set_option(option, value)
        except ValueError:
            print(self.fail + "Invalid input format. Expected 'option value'.")

    def handle_other_commands(self, command: str, user_input: str):
        if self.current_command and command in SubCommands.subcmds.get(self.current_command, {}):
            self.sub_command_handler(command)
        else:
            print(self.fail + "Unknown command or not in the correct context")

    def show_options(self):
        # Simplified for clarity, implement the logic as per your requirements
        print(self.success + "Showing options for command: " + self.current_command)

    def set_option(self, option: str, value: str):
        # Simplified for clarity, implement the logic as per your requirements
        print(self.success + "Option " + option + " set to " + value)


def main():
    banner = colored('''┏┳┓┏┓┓ ┏┓┳┓  ┏┓┏┓''', 'green') + '''\n'''
    banner += colored(''' ┃ ┣┫┃ ┃┃┃┃  ┃ ┏┛''', 'light_green') + '''\n'''
    banner += colored(''' ┻ ┛┗┗┛┗┛┛┗  ┗┛┗━''', 'light_yellow') + '''\n'''
    banner += colored('''https://github.com/Cleck777/Talon              v2.0''', 'white') + '''\n'''
    
    style = Style.from_dict({
        'prompt': '#ff6b6b',  # Example style
    })
    
    talon = Talon()  # Create an instance of Talon
    print(banner)
    session = PromptSession(history=InMemoryHistory())
    
    try:
        while True:
            # Dynamically create the prompt based on the current command
            if talon.current_command:
                prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> <ansiwhite>[</ansiwhite><ansired>{command}</ansired><ansiwhite>] > </ansiwhite>'.format(
                    username=ServerCommands.SList["settings"]["Options"]["Username"]["Value"], 
                    ip=ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"], 
                    command=talon.current_command))
            else:
                prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> '.format(
                    username=ServerCommands.SList["settings"]["Options"]["Username"]["Value"], 
                    ip=ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"]))
            
            # Read user input
            user_input = session.prompt(prompt_text, style=style)
            talon.input_handler(user_input)

    except KeyboardInterrupt:
        print(talon.success + random.choice(farewells))
        exit()

if __name__ == "__main__":
    main()