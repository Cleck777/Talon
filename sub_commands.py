from MTLS_Controller import MTLS_Controller

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
            }
        }
    }