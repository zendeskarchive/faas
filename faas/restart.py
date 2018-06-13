import os

from faas import app
from faas.utils import set_crash_loop, get_crash_loop_file_identifier
from faas.auth_wrapper import verify_token
from flask import request


@app.route('/restart')
@verify_token()
def restart():
    exit_code = request.args.get('exit_code', default=0, type=int)
    crash_loop = request.args.get('crash_loop', default=False)
    if crash_loop:
        set_crash_loop(get_crash_loop_file_identifier())
    os._exit(exit_code)
