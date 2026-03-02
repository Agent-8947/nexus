import os
import sys
import json
import time
import win32file
import pywintypes
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- CONFIGURATION ---
PIPE_NAME = r'\\.\pipe\ide-optimus-core'
HTTP_PORT = 5000

app = Flask(__name__)
CORS(app) # Enable CORS for landing page interaction

def send_to_pipe(message):
    """
    Sends a string message to the Windows Named Pipe.
    """
    try:
        # Open the pipe as a client
        handle = win32file.CreateFile(
            PIPE_NAME,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0, None,
            win32file.OPEN_EXISTING,
            0, None
        )
        # Write to pipe
        win32file.WriteFile(handle, message.encode())
        win32file.CloseHandle(handle)
        return True
    except pywintypes.error as e:
        print(f"Pipe Error: {e}")
        return False

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    cmd = data.get('command', 'TEST_PING')
    print(f"[*] API received command: {cmd}")
    
    success = send_to_pipe(cmd)
    
    if success:
        return jsonify({"status": "SUCCESS", "message": f"Command '{cmd}' injected into Pipe"}), 200
    else:
        return jsonify({"status": "ERROR", "message": "Pipe Server Offline"}), 500

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "BRIDGE_ACTIVE", "pipe": PIPE_NAME}), 200

if __name__ == "__main__":
    print(f"=== IDE OPTIMUS API BRIDGE STARTING ===")
    print(f"[*] Endpoint: http://localhost:{HTTP_PORT}/command")
    print(f"[*] Targeting Pipe: {PIPE_NAME}")
    app.run(port=HTTP_PORT, debug=False)
