from __future__ import print_function

import time
from faas import app
from faas.auth_wrapper import verify_token
from flask import request
from flask import g


@app.before_request
def parse_global_args():
    functions = list()
    delay = request.args.get('delay', default=0, type=int)
    g.return_status_code = request.args.get(
        'return_status_code', default=None, type=int
    )
    functions.append((time.sleep, [delay]))

    for func, args in functions:
        print("Executing {}({})".format(func.__name__, *args))
        func(*args)


@app.after_request
def return_status_code(response):
    if g.return_status_code:
        response.status_code = g.return_status_code
    return response


@app.route('/')
@verify_token()
def index():
    return 'Sup yo?'


@app.route('/ping')
def ping():
    return 'pong'
