from MTLS_Controller import MTLS_Controller
from HTTPS_Controller import HTTPS_Controller
from server_commands import ServerCommands 
import ImplantCompiler
import proxy_controller

class SubCommands:
    subcmds = {
        'MTLS' : {
            "start" : {
                "Description" : "Start the mTLS server",
                "Location" : lambda: MTLS_Controller.start()
            },
            "generate" : {
                "Description" : "Generate mTLS certificates",
                "Location" : lambda: MTLS_Controller.generate_mtls_certificates()
            },
        },

        'HTTPS' : {
            "start" : {
                "Description" : "Start the HTTPS server",
                "Location" : lambda: HTTPS_Controller.start()
            },
            "generate" : {
                "Description" : "Generate HTTPS certificates",
                "Location" : lambda: HTTPS_Controller.generate_https_certificates()
            }

        },

        'Implant' : {
            "geenerate" : {
                "Description" : "Compile the implant",
                "Location" : lambda: ImplantCompiler.compile_implant(ServerCommands.SList["Implant"]["Options"]["SourcePath"]["Value"], ServerCommands.SList["Implant"]["Options"]["OperatingSystem"]["Value"], ServerCommands.SList["Implant"]["Options"]["BinaryPath"]["Value"])
            },
            "serve" : {
                "Description" : "Serve the implant",
                "Location" : lambda: ImplantCompiler.serve_implant()
            },
        },
        'Proxy' : {
            "start" : {
                "Description" : "Start the Proxy server with the given host and port",
                "Location" : lambda: proxy_controller.StartProxy()
            }

        }
    
    }

