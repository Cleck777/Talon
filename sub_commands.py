from MTLS_Controller import MTLS_Controller
from HTTPS_Controller import HTTPS_Controller
import ImplantCompiler
import 

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
            "generate" : {
                "Description" : "Compile the implant",
                "Location" : lambda: ImplantCompiler.compile_implant()
            }
        }
    
}