import os
from OptionsTable import OptionsTable
from HelpTable import HelpTable


class ServerCommands:
    
    
    AdvancedTable = HelpTable("Advanced Commands", ["Command", "Description"])
    HelperTable = HelpTable("Generic Commands", ["Command", "Description"])
    SettingsTable = OptionsTable("Settings", ["Setting", "Value", "Required", "Description"])
    CrackTable = OptionsTable("Password Cracking", ["Setting", "Value", "Required", "Description"])
    MTLSTable = OptionsTable("MTLS", ["Setting", "Value", "Required", "Description"])
    HTTPSTable = OptionsTable("HTTPS", ["Setting", "Value", "Required", "Description"])
    
    
    ServList = {
        "show": {
            "Description": "Show information",
            "Options": {
                "Options": ""
            }
        },
        "use": {
            "Description": "Use a command",
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
                    "Description": "Username",
                    "Location": 0
                },
                "Server_IP": {
                    "Value": "localhost",
                    "Required": "Yes",
                    "Description": "Username",
                    "Location": 1
                },
                "Server_Port": {
                    "Value": "9091",
                    "Required": "Yes",
                    "Description": "Username",
                    "Location": 2
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
                    "Description": "Path of the hashes for cracking",
                    "Location": 0
                },
                "Wordlist": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path of the Wordlist typically found in /etc/wordlists",
                    "Location": 1
                },
                "Hash_Type":{
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Number for the hash type in relation to number described in hashcat",
                    "Location": 2
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
                    "Description": "Path to the CA Certificate",
                    "Location": 0
                },
                "SERVER_CERT": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path to the Server Certificate",
                    "Location": 1
                },
                "SERVER_KEY": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path to the Server Key",
                    "Location": 2
                },
                "IP": {
                    "Value" : "192.168.1.165",
                    "Required": "Yes",
                    "Description": "IP Address for the server",
                    "Location": 3
                },
                "Port": {
                    "Value" : "9091",
                    "Required": "Yes",
                    "Description": "Port for the server",
                    "Location": 4
                }
            },
            "Table": MTLSTable,
            
            
        },
        "HTTPS": {
            "Description": "Start the HTTPS server with the given host and port",
            "Options": {
                "SERVER_CERT": {
                    "Value" : "https/server.crt",
                    "Required": "Yes",
                    "Description": "Path to the Server Certificate",
                    "Location": 0
                },
                "SERVER_KEY": {
                    "Value" : "https/server.key",
                    "Required": "Yes",
                    "Description": "Path to the Server Key",
                    "Location": 1
                },
                "IP": {
                    "Value" : "192.168.112.145",
                    "Required": "Yes",
                    "Description": "IP Address for the server",
                    "Location": 2
                },
                "Port": {
                    "Value" : "9091",
                    "Required": "Yes",
                    "Description": "Port for the server",
                    "Location": 3
                }
            },
            "Table": HTTPSTable
    }
    }
    if SList["settings"]["Options"]["Username"]["Value"] == "":
            try:
                SList["settings"]["Options"]["Username"]["Value"] = os.getlogin()
            except:
                SList["settings"]["Options"]["Username"]["Value"] = ""
    if SList["settings"]["Options"]["Server_IP"]["Value"] == "":
       SList["settings"]["Options"]["Server_IP"]["Value"] = "localhost"

    def update_mtls_ip_port(self, ip, port):
        self.SList["MTLS"]["Options"]["IP"]["Value"] = ip
        self.SList["MTLS"]["Options"]["Port"]["Value"] = port

    def __init__(self):
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
        