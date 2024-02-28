import socket
import ssl
from threading import Thread

class MTLS_Server:
    def __init__(self, ca_cert, server_cert, server_key):
        self.ca_cert = ca_cert
        self.server_cert = server_cert
        self.server_key = server_key

    def start_server(self, host, port):
        """Initialize and start the mTLS server."""
        context = self._setup_ssl_context()
        server_thread = Thread(target=self._run_server, args=(context, host, port), daemon=True)
        server_thread.start()
        print(f"mTLS server started on {host}:{port}")
        return server_thread

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
            sock.bind((host, port))
            sock.listen(5)
            with context.wrap_socket(sock, server_side=True) as ssock:
                print(f"mTLS server listening on {host}:{port}")
                while True:
                    try:
                        connection, address = ssock.accept()
                        print(f"Secure connection from {address}")
                        # Handle the connection or spawn a new thread to do so
                    except Exception as e:
                        print(f"Server error: {e}")
