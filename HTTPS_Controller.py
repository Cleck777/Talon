import ssl
import subprocess
import os
from CertBuilder import CertBuilder
from HTTPS_Server import HTTPS_Server  # Assume you have a similar server setup for HTTPS
from server_commands import ServerCommands
from termcolor import colored

class HTTPS_Controller:
    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    server_commands = ServerCommands
    https_options = server_commands.SList["HTTPS"]["Options"]
    https_server = HTTPS_Server(https_options["SERVER_CERT"]["Value"], https_options["SERVER_KEY"]["Value"])

    @staticmethod
    def start_https_server():
        """Starts the HTTPS server with the given host and port."""
        try:
            HTTPS_Controller.https_server.start_server(HTTPS_Controller.https_options["IP"]["Value"], int(HTTPS_Controller.https_options["Port"]["Value"]))
        except ValueError:
            print(HTTPS_Controller.fail + "Invalid port number.")

    @staticmethod
    def show_connections():
        """Display the current connections to the HTTPS server."""
        print("HTTPS Connections:")
        for i, connection in enumerate(HTTPS_Controller.https_server.connection_pool):
            print(f"  {i + 1}. {connection}")

    @staticmethod
    def generate_https_certificates(folder_name="HTTPS_certs"):
        cert_builder = CertBuilder()
        cert_builder.setup_https()  # Assuming a similar method exists for HTTPS setup

        '''# Create the directory for storing certificates and keys
        os.makedirs(folder_name, exist_ok=True)

        # Define paths for the output files within the new folder
        server_key = os.path.join(folder_name, "server.key")
        server_csr = os.path.join(folder_name, "server.csr")
        server_cert = os.path.join(folder_name, "server.crt")

        # Generate the server key and certificate signing request (CSR)
        subprocess.run(["openssl", "req", "-newkey", "rsa:2048", "-nodes",
                        "-keyout", server_key, "-out", server_csr, "-subj", "/CN=myserver.com"], check=True)

        # Sign the server CSR to create the server certificate
        subprocess.run(["openssl", "x509", "-req", "-days", "365", "-in", server_csr,
                        "-signkey", server_key, "-out", server_cert], check=True)

        print(HTTPS_Controller.success + "Certificates and keys generated successfully in " + folder_name + " folder.")
        HTTPS_Controller.server_commands.SList["HTTPS"]["Options"]["SERVER_CERT"]["Value"] = os.path.join(folder_name, "server.crt")
        HTTPS_Controller.server_commands.SList["HTTPS"]["Options"]["SERVER_KEY"]["Value"] = os.path.join(folder_name, "server.key")'''
    @staticmethod
    def start():
        print("Starting HTTPS Server on " + HTTPS_Controller.server_commands.SList["HTTPS"]["Options"]["IP"]["Value"] + ":" + HTTPS_Controller.server_commands.SList["HTTPS"]["Options"]["Port"]["Value"] + "...")
        HTTPS_Controller.start_https_server()

    @staticmethod
    def test():
        return print("Testing HTTPS Server...")
