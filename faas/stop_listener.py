import os
from faas import app
from faas.auth_wrapper import verify_token
from flask import request


@app.route('/stop_listener')
@verify_token()
def stop_listener():
    os.environ['WERKZEUG_RUN_MAIN'] = 'false'
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Stopping listener"
