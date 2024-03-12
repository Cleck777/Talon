import ssl
from CertBuilder import CertBuilder
from MTLS_Server import MTLS_Server
from server_commands import ServerCommands  
from termcolor import colored
import subprocess
import os

class MTLS_Controller:
    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    server_commands = ServerCommands
    mtls_options = server_commands.SList["MTLS"]["Options"]
    mtls_server = MTLS_Server(mtls_options["CA_CERT"]["Value"], mtls_options["SERVER_CERT"]["Value"], mtls_options["SERVER_KEY"]["Value"])

    @staticmethod
    def start_mtls_server():
        """Starts the mTLS server with the given host and port."""
        try:
            MTLS_Controller.mtls_server.start_server(MTLS_Controller.mtls_options["IP"]["Value"], int(MTLS_Controller.mtls_options["Port"]["Value"]))
        except ValueError:
            print("Invalid port number.")
    @staticmethod
    def show_connections():
        """Display the current connections to the mTLS server."""
        print("Connections:")
        for i, connection in enumerate(MTLS_Controller.mtls_server.connection_pool):
            print(f"  {i + 1}. {connection.getpeername()}")
    
    @staticmethod
    def generate_mtls_certificates(folder_name="certs"):

        cert_builder = CertBuilder()
        cert_builder.setup_mtls()

        """
       
        # Create the directory for storing certificates and keys
        os.makedirs(folder_name, exist_ok=True)

        # Define paths for the output files within the new folder
        ca_key = os.path.join(folder_name, "ca.key")
        ca_cert = os.path.join(folder_name, "ca.crt")
        server_key = os.path.join(folder_name, "server.key")
        server_csr = os.path.join(folder_name, "server.csr")
        server_cert = os.path.join(folder_name, "server.crt")
        client_key = os.path.join(folder_name, "client.key")
        client_csr = os.path.join(folder_name, "client.csr")
        client_cert = os.path.join(folder_name, "client.crt")

        # Generate the CA key and certificate
        subprocess.run(["openssl", "req", "-new", "-x509", "-days", "3650",
                        "-keyout", ca_key, "-out", ca_cert, "-subj", "/CN=My CA"], check=True)

        # Generate the server key and certificate signing request (CSR)
        subprocess.run(["openssl", "req", "-newkey", "rsa:2048", "-nodes",
                        "-keyout", server_key, "-out", server_csr, "-subj", "/CN=myserver.com"], check=True)

        # Sign the server CSR with the CA key (creating the server certificate)
        subprocess.run(["openssl", "x509", "-req", "-days", "365", "-in", server_csr,
                        "-CA", ca_cert, "-CAkey", ca_key, "-set_serial", "01", "-out", server_cert], check=True)

        # Generate the client key and CSR
        subprocess.run(["openssl", "req", "-newkey", "rsa:2048", "-nodes",
                        "-keyout", client_key, "-out", client_csr, "-subj", "/CN=myclient"], check=True)

        # Sign the client CSR with the CA key (creating the client certificate)
        subprocess.run(["openssl", "x509", "-req", "-days", "365", "-in", client_csr,
                        "-CA", ca_cert, "-CAkey", ca_key, "-set_serial", "02", "-out", client_cert], check=True)

        print(MTLS_Controller.success + "Certificates and keys generated successfully in " + folder_name + "folder.")
        MTLS_Controller.server_commands.SList["MTLS"]["Options"]["CA_CERT"]["Value"] = folder_name + "/ca.crt"
        MTLS_Controller.server_commands.SList["MTLS"]["Options"]["SERVER_CERT"]["Value"] = folder_name + "/server.crt"
        MTLS_Controller.server_commands.SList["MTLS"]["Options"]["SERVER_KEY"]["Value"] = folder_name + "/server.key"
        """
        
    @staticmethod
    def start():
            print("Starting mTLS Server on " + MTLS_Controller.server_commands.SList["MTLS"]["Options"]["IP"]["Value"] + ":" + MTLS_Controller.server_commands.SList["MTLS"]["Options"]["Port"]["Value"] + "...")
            MTLS_Controller.start_mtls_server()
    @staticmethod
    def test():
        return print("Testing mTLS Server...")
        
