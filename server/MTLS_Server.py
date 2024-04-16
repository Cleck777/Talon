import socket
import ssl
from threading import Thread
import multiprocessing
import logging
from termcolor import colored

class MTLS_Server:
    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    connection_pool = []

    def __init__(self, ca_cert, server_cert, server_key):
        self.ca_cert = "./cert/ca.pem"
        self.server_cert = "./cert/server.crt"
        self.server_key = "./cert/server.key"
        self.server_process = None

    def start_server(self, host, port):
        """Initialize and start the mTLS server."""
        context = self._setup_ssl_context()
        if context is None:
            return
        self.server_process = multiprocessing.Process(target=self._run_server, args=(context, host, port), daemon=True)
        try:
            self.server_process.start()
        except Exception as e:
            logging.error("Server error: " + str(e))
        logging.info(f"mTLS server started on {host}:{port}")

    def _setup_ssl_context(self):
        """Set up SSL context for mTLS."""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.server_cert, keyfile=self.server_key)
        context.load_verify_locations(cafile=self.ca_cert)
        context.verify_mode = ssl.CERT_REQUIRED
        return context

    def _run_server(self, context, host, port):
        """Run the mTLS server to handle client connections."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
                sock.listen(5)
                with context.wrap_socket(sock, server_side=True) as ssock:
                    logging.info(f"mTLS server listening on {host}:{port}")
                    while True:
                        try:
                            connection, address = ssock.accept()
                            connected_msg = "💀 " + colored(f'Secure connection from {address}', 'red')
                            logging.info(connected_msg)
                            self.connection_pool.append(connection)
                            # Spawn a new thread to handle the connection
                            thread = Thread(target=self._handle_connection, args=(connection,))
                            thread.start()
                        except Exception as e:
                            logging.error(f"Server error: {e}")
            except Exception as e:
                logging.error(f"Socket error: {e}")

    def _handle_connection(self, connection):
        """Handle a client connection."""
        try:
            # Receive data from the client
            data = connection.recv(1024)
            if data:
                return_msg = "💀 " + colored(f'Received data: {data.decode()}', 'blue')
                logging.info(return_msg)
                # Send a response back to the client
                connection.sendall(b"Hello! you have been infected by Talon")
        except Exception as e:
            logging.error(f"Error handling connection: {e}")
        finally:
            connection.close()
