import socket
import ssl
import os
import subprocess
from threading import Thread, Lock
import logging
from termcolor import colored
import CertBuilder
from http.server import BaseHTTPRequestHandler
from ConnectionManager import ConnectionManager
from io import BytesIO
import select
class HTTPS_Server:
    """
    Represents an HTTPS server that handles client connections.

    Attributes:
        success (str): A colored string representing a success message.
        fail (str): A colored string representing a failure message.
        connection_pool (list): A list to store client connections.

    Methods:
        __init__(self, server_cert, server_key): Initializes the HTTPS_Server object.
        start_server(self, host, port): Initializes and starts the HTTPS server.
        _setup_ssl_context(self): Sets up the SSL context for HTTPS.
        _run_server(self, context, host, port): Runs the HTTPS server to handle client connections.
        generate_https_certificates(self, folder_name="MTLS_certs"): Generates HTTPS certificates.
        execute_command(self, command): Executes a command and returns the output.
        upload_file(self, file_path, data): Uploads a file with the given data.
        download_file(self, file_path): Downloads the contents of a file.
        _handle_connection(self, connection, address): Handles a client connection.
        handle_getcmd(self, client_socket, method): Handles a GET command.
        handle_cmdoutput(self, client_socket, method, request): Handles a POST command.
    """

    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    connection_pool = []

    def __init__(self, server_cert, server_key):
        self.connection_manager = ConnectionManager()
        self.server_cert = "./cert/server.crt"
        self.server_key = "./cert/server.key"
        self.lock = Lock()
        self.server_process = None

    def start_server(self, host, port):
        """Initialize and start the HTTPS server."""
        context = self._setup_ssl_context()
        if context is None:
            return
        self.server_process = Thread(target=self._run_server, args=(context, host, port), daemon=True)
        try:
            self.server_process.start()
        except Exception as e:
            logging.error("Server error: " + str(e))
        logging.info(f"HTTPS server started on {host}:{port}")

   
    def _setup_ssl_context(self):
        """Set up SSL context for HTTPS."""
        if not os.path.isfile(self.server_cert) or not os.path.isfile(self.server_key):
            raise FileNotFoundError("Server certificate or key file not found.")
        
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.server_cert, keyfile=self.server_key)
        context.verify_mode = ssl.CERT_NONE
        return context
    

    def _run_server(self, context, host, port):
        """Run the HTTPS server to handle client connections."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
            sock.listen(5)
            with context.wrap_socket(sock, server_side=True) as ssock:
                logging.info(f"HTTPS server listening on {host}:{port}")
                while True:
                    try:
                        connection, address = ssock.accept()
                        conn_id = self.connection_manager.add_connection(connection, address)
                        logging.info(f"Secure connection from {address}, assigned ID {conn_id}")
                        thread = Thread(target=self._handle_connection, args=(conn_id,))
                        thread.start()
                    except Exception as e:
                        logging.error(f"Server error: {e}")

    

    def generate_https_certificates(self, folder_name="MTLS_certs"):
        """
        Generates HTTPS certificates.

        Args:
            folder_name (str): The name of the folder to store the certificates.

        Returns:
            None
        """
        cert_builder = CertBuilder()
        cert_builder.setup_mtls()

    def execute_command(self, command):
        """
        Executes a command and returns the output.

        Args:
            command (str): The command to execute.

        Returns:
            str: The output of the command.
        """
        return subprocess.check_output(command, shell=True).decode()

    def upload_file(self, file_path, data):
        """
        Uploads a file with the given data.

        Args:
            file_path (str): The path of the file to upload.
            data (bytes): The data to write to the file.

        Returns:
            None
        """
        with open(file_path, "wb") as file:
            file.write(data)

    def download_file(self, file_path):
        """
        Downloads the contents of a file.

        Args:
            file_path (str): The path of the file to download.

        Returns:
            bytes: The contents of the file.
        """
        with open(file_path, "rb") as file:
            return file.read()
    def _handle_connection(self, conn_id):
        """Handle the connection identified by conn_id."""
        conn_details = self.connection_manager.get_connection(conn_id)
        if conn_details is None:
            logging.error(f"Connection ID {conn_id} not found.")
            return

        connection = conn_details['connection']
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1)
        address = conn_details['address']
        logging.info(f"Handling connection {conn_id} from {address}")

        try:
            # Example of a simple data handling loop
            # Modify as needed based on your specific requirements
            while conn_details['active']:
                data = connection.recv(1024)
                if not data:
                    # No data, client closed the connection
                    break
                # Process the data...
                logging.info(f"Received data from {address}: {data.decode('utf-8')}")
                # Respond to the data...
                response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"
                connection.sendall(response)
        except Exception as e:
            logging.error(f"Error handling connection {conn_id} from {address}: {e}")
        finally:
            # Close the connection and remove it from the connection manager
            connection.close()
            self.connection_manager.remove_connection(conn_id)
            logging.info(f"Closed connection {conn_id} from {address}")


    def handle_getcmd(self, client_socket, method):
        """
        Handles a GET command.

        Args:
            client_socket (socket): The client socket.
            method (str): The HTTP method.

        Returns:
            None
        """
        if method == 'GET':
            try:
                # Simulate waiting for command input from the user
                command = input("[+] CMD > ")
                # Validate the command
                if not self._validate_command(command):
                    logging.error("Invalid command")
                    return
                response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(command)}\r\n\r\n{command}"
                client_socket.sendall(response.encode('utf-8'))
            except BrokenPipeError:
                logging.error("Client closed the connection")
            except Exception as e:
                logging.error(f"Failed to handle GET command: {e}")

    def _validate_command(self, command):
        """
        Validates a command.

        Args:
            command (str): The command to validate.

        Returns:
            bool: True if the command is valid, False otherwise.
        """
        # Add your validation logic here
        return True

    def handle_cmdoutput(self, client_socket, method, request):
        """
        Handles a POST command.

        Args:
            client_socket (socket): The client socket.
            method (str): The HTTP method.
            request (str): The HTTP request.

        Returns:
            None
        """
        if method == 'POST':
            _, body = request.split('\r\n\r\n')
            print(f"[+] Got response:\n{body}")
            response = "HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"
            client_socket.sendall(response.encode('utf-8'))
