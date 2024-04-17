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
from ConnectionManager import ConnectionManager
from sub_commands import SubCommands
from MTLS_Controller import MTLS_Controller
from HTTPS_Controller import HTTPS_Controller
import subprocess
import os

class Talon:
    ServerCommands()
    SubCommands()
    current_command = ""
    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    
    def __init__(self):
        self.is_interacting = False
        self.active_connection_id = None



    def sub_command_handler(self, command: str) -> None:
        if command in SubCommands.subcmds[self.current_command]:
            SubCommands.subcmds[self.current_command][command]["Location"]()
        else:
            self.input_handler(command)
    
    def input_handler(self, user_input: str) -> None:
        parts = user_input.split(maxsplit=1)
        if len(parts) == 0:
            
            return
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""

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
        elif command == "Implant":
            self.current_command = "Implant"  
        elif command == "use":
            print(args)
            command2 = args.split(" ")[0]
            if not command2:
                    print(self.fail + "Please state what you would like to use")
                    return
            args2 = args.split(" ")[1]
            if command2 == "connection":
                print(args2)
                self.use_connection(args2)
            else:
                print(self.fail + "No command selected")
        elif command == "MTLS":
            self.current_command = "MTLS"
        elif command == "HTTPS":
            self.current_command = "HTTPS"
        elif command == "Proxy":
            self.current_command = "Proxy"
        elif command == "back":
            self.current_command = None
        elif command == "show":
            if not args:
                print(self.fail + "Please state what you would like to show")
                return
            if args == "options" and self.current_command:
                self.show_options()
            if args == "connections":
                self.show_connections()
           # else: 
                #print(self.fail + "No command selected")
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
            print(self.fail + "No command selected or no options available for the current command.")
            return
        table = ServerCommands.SList[self.current_command]["Table"]
        table.display()
        try:
            if SubCommands.subcmds[self.current_command]:
                print(self.success + "Sub Commands:")
                for subcommand in SubCommands.subcmds[self.current_command]:
                    print(" - " + subcommand)
        except:
            pass
    def show_connections(self):
        active_connections = HTTPS_Controller.https_server.connection_manager.list_active_connections()
        if active_connections:
            print(self.success + "Active connections:")
            for conn_id, address, is_active in active_connections:
                print(f"ID: {conn_id}, Address: {address}, Active: {is_active}")
        else:
            print(self.fail + "No active connections.")
    def use_connection(self, name: str):
        # Find the connection by name/address or index
        # For simplicity, assume 'name' is an index for now
        try:
            conn_id = int(name)  # Convert name to integer to get the connection ID
            # Directly check if conn_id is a valid key in the connections dictionary
            if conn_id in HTTPS_Controller.https_server.connection_manager.connections:
                # If valid, proceed to interact with the connection
                # You may want to call another method here that actually handles the interaction
                
                self.interact_with_connection(conn_id)
                # Example: self.interact_with_connection(conn_id)
            else:
                print(f"Connection ID {conn_id} not found.")
        except ValueError:
            print("Invalid connection identifier. Please use a numeric ID.")


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


    def interact_with_connection(self, conn_id):
        """Initiates an interaction session with the specified connection."""
        session = PromptSession(history=InMemoryHistory())
        prompt_text = HTML(f'<ansigreen>TALON {Talon.active_connection_id}></ansigreen> CLI> ')
        self.is_interacting = True
        self.active_connection_id = conn_id
        connection_details = HTTPS_Controller.https_server.connection_manager.get_connection(conn_id)
    
        if connection_details is None:
            print(self.fail + f"Connection {conn_id} not found.")
            self.is_interacting = False
            return
        
        connection = connection_details['connection']
        print(colored(f"Now interacting with connection {conn_id}. Type 'exit' to end session.", 'green'))
        
        while self.is_interacting:
            user_input = session.prompt(prompt_text)
            if user_input.strip().lower() == 'exit':
                self.exit_interaction()
                break
            try:
                print("sending")
                print(user_input)
                connection.sendall(user_input.encode() + b'\n')  # Ensure newline for client-side processing
            except Exception as e:
                print(self.fail + f"Failed to send command: {e}")
                self.exit_interaction()

    def send_command_to_connection(self, command):
        """Sends a command to the active connection."""
        if not self.is_interacting or self.active_connection_id is None:
            print(self.fail + "Not currently interacting with a connection.")
            return

        connection_details = HTTPS_Controller.https_server.connection_manager.get_connection(self.active_connection_id)
        if connection_details is None:
            print(self.fail + f"Connection {self.active_connection_id} not found.")
            return

        connection = connection_details['connection']
        try:
            # Sending command
            connection.sendall(command.encode('utf-8'))
            print(self.success + f"Command sent to connection {self.active_connection_id}.")
            # Example of receiving a response, adjust as necessary
            response = connection.recv(1024).decode('utf-8')
            print(f"Response: {response}")
        except Exception as e:
            print(self.fail + f"Failed to send command: {e}")
    def exit_interaction(self):
        """Exits the interaction mode."""
        self.is_interacting = False
        self.active_connection_id = None
        print(colored("Exited interaction mode.", 'green'))
            


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
    try:
        subprocess.run(['go', 'mod', 'init',  'github.com/Cleck777/Talon/Talon_Implant'], check=True)  # Initialize Go module
    except subprocess.CalledProcessError as e:
      
        pass
    session = PromptSession(history=InMemoryHistory())
    try:
        while True:
            if Talon.is_interacting:
                # Change the prompt to indicate interaction mode
                prompt_text = HTML(f'<ansigreen>TALON {Talon.active_connection_id}></ansigreen> CLI> ')
            else:
                if Talon.current_command:
                
                    prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> <ansiwhite>[</ansiwhite><ansired>{command}</ansired><ansiwhite>] > </ansiwhite>'.format(username=username, ip=ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"], command=Talon.current_command))
                else:
                    prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> '.format(username=ServerCommands.SList["settings"]["Options"]["Username"]["Value"], ip=ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"]))
                # Use prompt_toolkit's session to read input with support for history
            
            user_input = session.prompt(prompt_text)

            if Talon.is_interacting:
                if user_input.strip().lower() == 'exit':
                    Talon.exit_interaction()
                    continue
                Talon.send_command_to_connection(user_input)
            else:
            
                Talon.input_handler(user_input)
    except KeyboardInterrupt:
        print(Talon.success + random.choice(farewells))

        exit()
