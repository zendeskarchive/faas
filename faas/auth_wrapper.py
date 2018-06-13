from functools import wraps
from flask import g
from flask import request
import faas


def verify_token():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if faas.require_authentication:
                application_token = request.args.get(
                    'application_token', default=""
                )
                if application_token not in faas.application_tokens:
                    g.return_status_code = 401
                    return "Invalid application_token"
            return f(*args, **kwargs)
        return wrapped
    return wrapper
