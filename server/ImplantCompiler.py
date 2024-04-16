import subprocess

from termcolor import colored
import os
import subprocess
import socketserver
import signal
import http.server


success = colored('[+] ', 'green')
fail = colored('[-] ', 'red')
info = colored('[*] ', 'blue')
def compile_implant(sourcePath, OperatingSystem, BinaryPath):
    if OperatingSystem == 'Windows':
        en = os.environ.copy()
        en['GOOS'] = 'windows'
        en['GOARCH'] = 'amd64'

        print(f"{info} Compiling implant for Windows")

        compile_code = ['go', 'build', '-o', BinaryPath + '.exe', sourcePath]
    elif OperatingSystem in ["Linux", "Darwin"]:  # Darwin is macOS
        compile_code = ['go', 'build', '-o', BinaryPath, sourcePath]
    else:
        return f"Unsupported OS: {OperatingSystem}"
    try:
        os.chdir('../Talon_Implant')  # Move into the ../Talon_Implant directory
        print(f"{info} Compiling implant with command: {' '.join(compile_code)}")
        result = subprocess.Popen(compile_code, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=en)
        print(f"{success} Implant compiled successfully!")
        return result.stdout.read().decode('utf-8')  # Decode from bytes to string for readability
    except subprocess.CalledProcessError as e:
        print(f"{fail} Error compiling implant: {e.stderr.decode('utf-8')}")
        return   # Decode from bytes to string for readability
def serve_implant():
    PORT = 80  # Specify the port number you want to use
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        os.chdir('../Talon_Implant/Talon_Implant')  # Move into the ../Talon_Implant/Talon_Implant directory
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Server started on port {PORT}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("Server stopped by user")
                httpd.shutdown()
    except OSError as e:
        print(fail + "Error starting server: "+ e.strerror.decode('utf-8'))
        return  

    