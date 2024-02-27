import ssl
from CertBuilder import CertBuilder
from MTLS_Server import MTLS_Server
class MTLS_Controller:
    command_options = {
        "MTLS": {
            "CA_CERT": "",
            "SERVER_CERT": "",
            "SERVER_KEY": ""
        }
    }

    @staticmethod
    def start_mtls_server(host: str, port_str: str):
        """Starts the mTLS server with the given host and port."""
        try:
            port = int(port_str)
            mtls_options = self.command_options["MTLS"]
            mtls_server = MTLS_Server(mtls_options["CA_CERT"], mtls_options["SERVER_CERT"], mtls_options["SERVER_KEY"])
            mtls_server.start_server(host, port)
        except ValueError:
            print("Invalid port number.")
    @staticmethod
    def set_mtls_options(ca_cert: str, server_cert: str, server_key: str):
        """Sets the mTLS options."""
        MTLS_Controller.command_options["MTLS"]["CA_CERT"] = ca_cert
        MTLS_Controller.command_options["MTLS"]["SERVER_CERT"] = server_cert
        MTLS_Controller.command_options["MTLS"]["SERVER_KEY"] = server_key
        print("mTLS options set.")
    @staticmethod
    def generate_mtls_certificates():
        print("Generating mTLS certificates...")
        ca_country = input("CA Country: ") 
        ca_state = input("CA State: ")
        ca_locality = input("CA Locality: ")
        ca_org = input("CA Organization: ")
        ca_common_name = input("CA Common Name: ")
        server_common_name = input("Server Common Name: ")
        validity_years = int(input("Certificate Validity (years): "))

        ca_cert_builder = CertBuilder(ca_country, ca_state, ca_locality, ca_org, ca_common_name, server_common_name, validity_years)

        ca_cert_builder.generate_ca_private_key()
        ca_cert_builder.generate_ca_certificate()
        ca_cert_builder.generate_server_private_key()
        ca_cert_builder.generate_server_certificate()

        ca_cert_builder.save_certificates()
        print("mTLS certificates generated and saved.")
    @staticmethod
    def run(command_registry):
        MTLS_Controller.set_mtls_options(command_registry["MTLS"]["setting"]["ca_cert"], command_registry["MTLS"]["setting"]["server_cert"], command_registry["MTLS"]["setting"]["server_key"])

        MTLS_Controller.start_mtls_server(command_registry["MTLS"]["setting"]["ip"], command_registry["MTLS"]["setting"]["port"])

