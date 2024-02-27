import os

class CertBuilder:
    def __init__(self, ca_country, ca_state, ca_locality, ca_org, ca_common_name, server_common_name, validity_years=10, ca_private_key=None, ca_certificate=None, server_private_key=None, server_certificate=None, ):
        self.ca_country = ca_country
        self.ca_state = ca_state
        self.ca_locality = ca_locality
        self.ca_org = ca_org
        self.ca_common_name = ca_common_name
        self.server_common_name = server_common_name
        self.validity_years = validity_years
        self.ca_private_key = None
        self.ca_certificate = None
        self.server_private_key = None
        self.server_certificate = None
        public_exponent = 65537
        key_size = 2048

    def save_certificates_and_keys(self):
        # Create the "certs" directory if it doesn't exist
        os.makedirs("certs", exist_ok=True)

        # Serialize and save CA private key and certificate
        ca_private_key_pem = self.ca_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        ca_cert_pem = self.ca_certificate.public_bytes(serialization.Encoding.PEM)
        with open("certs/ca_private_key.pem", "wb") as f:
            f.write(ca_private_key_pem)
        with open("certs/ca_certificate.pem", "wb") as f:
            f.write(ca_cert_pem)

        # Serialize and save server private key and certificate
        server_private_key_pem = self.server_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        server_cert_pem = self.server_certificate.public_bytes(serialization.Encoding.PEM)
        with open("certs/server_private_key.pem", "wb") as f:
            f.write(server_private_key_pem)
        with open("certs/server_certificate.pem", "wb") as f:
            f.write(server_cert_pem)
