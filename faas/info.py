import os
import psutil
import socket

from faas import app
from faas.auth_wrapper import verify_token
from flask import jsonify


@app.route('/info')
@verify_token()
def info():
    output_json = {
        "pid": os.getpid(),
        "hostname": socket.gethostname(),
        "cwd": os.getcwd(),
        "memory": vars(psutil.Process(os.getpid()).memory_info())
    }
    return jsonify(output_json)
