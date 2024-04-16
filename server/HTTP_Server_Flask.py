from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
import os
import subprocess
import threading
import logging

app = Flask(__name__)
socketio = SocketIO(app)
clients = {}

# Directory for uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@socketio.on('connect')
def handle_connect():
    clients[request.sid] = {"address": request.remote_addr}
    logging.info(f"Client connected: {request.sid}, Address: {clients[request.sid]['address']}")

@socketio.on('disconnect')
def handle_disconnect():
    logging.info(f"Client disconnected: {request.sid}")
    del clients[request.sid]

@socketio.on('execute_command')
def handle_execute_command(data):
    command = data['command']
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
    emit('command_response', {'output': output})

@socketio.on('upload_file')
def handle_upload_file(data):
    file_data = data['file']  # Assume this is the binary content of the file
    file_path = os.path.join(UPLOAD_FOLDER, data['filename'])
    with open(file_path, 'wb') as f:
        f.write(file_data)
    emit('upload_response', {'message': f'File {data["filename"]} uploaded successfully'})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, certfile='path/to/server.crt', keyfile='path/to/server.key', port=4433)

