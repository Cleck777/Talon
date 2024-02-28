import os
from OptionsTable import OptionsTable
from HelpTable import HelpTable


class ServerCommands:
    
    
    AdvancedTable = HelpTable("Advanced Commands", ["Command", "Description"])
    HelperTable = HelpTable("Generic Commands", ["Command", "Description"])
    SettingsTable = OptionsTable("Settings", ["Setting", "Value", "Required", "Description"])
    CrackTable = OptionsTable("Password Cracking", ["Setting", "Value", "Required", "Description"])
    MTLSTable = OptionsTable("MTLS", ["Setting", "Value", "Required", "Description"])


    
    ServList = {
        "show": {
            "Description": "Show information",
            "Options": {
                "Options": ""
            }
        },
        "help": {
            "Description": "Display help menu"
        },
        "exit": {
            "Description": "Exit the program"
        },
        "back": {
            "Description": "Return to the previous command"
        },
    }
    SList = {
        "settings": {
            "Description": "Server settings",
            "Options": {
                "Username": {
                    "Value": "",
                    "Required": "Yes",
                    "Description": "Username"
                },
                "Server_IP": {
                    "Value": "",
                    "Required": "Yes",
                    "Description": "Username"
                },
                "Server_Port": {
                    "Value": "",
                    "Required": "Yes",
                    "Description": "Username"
                }
            },
            "Table": SettingsTable
        },
        "crack": {
            "Description": "Queue a hash",
            "Options": {
                "Hash_Location": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path of the hashes for cracking"
                },
                "Wordlist": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path of the Wordlist typically found in /etc/wordlists"
                },
                "Hash_Type":{
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Number for the hash type in relation to number described in hashcat"
                }
            },
            "Table": CrackTable
        },

        "MTLS": {
            "Description": "Starts the mTLS server with the given host and port",
            "Options": {
                "CA_CERT": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path to the CA Certificate"
                },
                "SERVER_CERT": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path to the Server Certificate"
                },
                "SERVER_KEY": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path to the Server Key"
                },
                "IP": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "IP Address for the server"
                },
                "Port": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Port for the server"
                }
            },
            "Table": MTLSTable,
            
            
        }
    }
    def update_mtls_ip_port(self, ip, port):
        self.SList["MTLS"]["Options"]["IP"]["Value"] = ip
        self.SList["MTLS"]["Options"]["Port"]["Value"] = port

    def __init__(self):
        if ServerCommands.SList["settings"]["Options"]["Username"]["Value"] == "":
            try:
                ServerCommands.SList["settings"]["Options"]["Username"]["Value"] = os.getlogin()
            except:
                ServerCommands.SList["settings"]["Options"]["Username"]["Value"] = ""
        if ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"] == "":
            ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"] = "localhost"

        for command in self.ServList:
            ServerCommands.HelperTable.add_row(command, ServerCommands.ServList[command]["Description"])
        for command in self.SList:
            ServerCommands.AdvancedTable.add_row(command, ServerCommands.SList[command]["Description"])

        for command in ServerCommands.SList:
            if "Options" in self.SList[command]:
                self.SList[command]["Table"] = OptionsTable(command, ["Option", "Value", "Required", "Description"])
                for option in self.SList[command]["Options"]:
                    option_data = self.SList[command]["Options"][option]
                    self.SList[command]["Table"].add_row(option, option_data["Value"], option_data["Required"], option_data["Description"])
        