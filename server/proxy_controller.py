# FILEPATH: proxy_controller.py
import subprocess
from server_commands import ServerCommands
from termcolor import colored
from enum import Enum








class ProxyType(Enum):
    WEBSOCKET = "websocket"
    TCP = "tcp"

class ProxyController:
    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    info = colored('[*] ', 'blue')

    def __init__(self, listen_address, port, password, tls, proxy_type, socks_address):
        self.listen_address = listen_address
        self.password = password
        self.port = port
        self.tls = tls
        self.proxy_type = proxy_type
        self.socks_address = socks_address

    def start_revsocks(self):
        command = ["revsocks"]

        if self.tls:
            command.append("-tls")
        if self.proxy_type == ProxyType.WEBSOCKET.value:
            command.append("-ws")
        elif self.proxy_type.lower() == ProxyType.TCP.value:
            command.append("-tcp")
        else:
            print(f"{self.fail} Invalid proxy type: {self.proxy_type}")
            return
        command.extend(["-listen", self.listen_address, "-socks", self.socks_address, "-pass", self.password])
        try:
            print(f"{self.info} Starting revsocks with command: {' '.join(command)}")
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except OSError as e:
            print(f"{self.fail} Failed to start revsocks: {e}")
# Example usage

    def stop_revsocks(self):
        if self.process:
            self.process.terminate()
            self.process = None
            print(f"{self.info} Stopped revsocks")
        else:
            print(f"{self.fail} revsocks is not running")

    def view_logs(self):
        if self.process:
            output = self.process.stdout.read().decode()
            print(f"{self.info} revsocks logs:\n{output}")
        else:
            print(f"{self.fail} revsocks is not running")

def start():
    Listen_Address = ServerCommands.SList["Proxy"]["Options"]["IP"]["Value"]
    Port = ServerCommands.SList["Proxy"]["Options"]["Port"]["Value"]
    Password = ServerCommands.SList["Proxy"]["Options"]["Password"]["Value"]
    TLS = ServerCommands.SList["Proxy"]["Options"]["TLS"]["Value"]
    Type = ServerCommands.SList["Proxy"]["Options"]["Type"]["Value"]
    Socks_Address = ServerCommands.SList["Proxy"]["Options"]["Socks_Address"]["Value"]

    proxy = ProxyController(Listen_Address, Port, Password, TLS, Type, Socks_Address)
    proxy.start_revsocks()
def stop():
   
    proxy.stop_revsocks()
def view_logs():
    proxy.view_logs()

Listen_Address = ServerCommands.SList["Proxy"]["Options"]["IP"]["Value"]
Port = ServerCommands.SList["Proxy"]["Options"]["Port"]["Value"]
Password = ServerCommands.SList["Proxy"]["Options"]["Password"]["Value"]
TLS = ServerCommands.SList["Proxy"]["Options"]["TLS"]["Value"]
Type = ServerCommands.SList["Proxy"]["Options"]["Type"]["Value"]
Socks_Address = ServerCommands.SList["Proxy"]["Options"]["Socks_Address"]["Value"]

proxy = ProxyController(Listen_Address, Port, Password, TLS, Type, Socks_Address)