import subprocess
import os
import base64
class CertBuilder:
    def run_command(self, command):
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stderr:
            print(f"Error: {result.stderr.decode()}")
        else:
            print(result.stdout.decode())

    def create_ca(self):
        print("Creating CA key and certificate...")
        self.run_command("openssl genrsa -out cert/ca.key 4096")
        self.run_command("openssl req -x509 -new -nodes -key cert/ca.key -sha256 -days 1024 -out cert/ca.pem -subj '/CN=Example CA'")

    def create_server_cert(self):
        print("Creating server key and certificate...")
        self.run_command("openssl genrsa -out cert/server.key 4096")
        self.run_command("openssl req -new -key cert/server.key -out cert/server.csr -subj '/CN=TalonServer'")
        self.run_command("openssl x509 -req -in cert/server.csr -CA cert/ca.pem -CAkey cert/ca.key -CAcreateserial -out cert/server.crt -days 500 -sha256")

    def create_client_cert(self):
        print("Creating client key and certificate...")
        self.run_command("openssl genrsa -out cert/client.key 4096")
        self.run_command("openssl req -new -key cert/client.key -out cert/client.csr -subj '/CN=example.client.com'")
        self.run_command("openssl x509 -req -in cert/client.csr -CA cert/ca.pem -CAkey cert/ca.key -CAcreateserial -out cert/client.crt -days 500 -sha256")

    def setup_mtls(self):
        os.makedirs("cert", exist_ok=True)
        self.create_ca()
        self.create_server_cert()
        self.create_client_cert()
        print("mTLS components created successfully.")

        # Encode certificates and keys in base64
        encoded_ca_key = base64.b64encode(open("cert/ca.key", "rb").read()).decode()
        encoded_ca_cert = base64.b64encode(open("cert/ca.pem", "rb").read()).decode()
        encoded_server_key = base64.b64encode(open("cert/server.key", "rb").read()).decode()
        encoded_server_cert = base64.b64encode(open("cert/server.crt", "rb").read()).decode()
        encoded_client_key = base64.b64encode(open("cert/client.key", "rb").read()).decode()
        encoded_client_cert = base64.b64encode(open("cert/client.crt", "rb").read()).decode()

        # Write encoded certificates and keys to a file
        with open("cert/certs_base64.txt", "w") as file:
            file.write(f"CA Key:\n{encoded_ca_key}\n\n")
            file.write(f"CA Certificate:\n{encoded_ca_cert}\n\n")
            file.write(f"Server Key:\n{encoded_server_key}\n\n")
            file.write(f"Server Certificate:\n{encoded_server_cert}\n\n")
            file.write(f"Client Key:\n{encoded_client_key}\n\n")
            file.write(f"Client Certificate:\n{encoded_client_cert}\n\n")

        print("Certificates and keys encoded in base64 and saved to 'certs_base64.txt'.")
