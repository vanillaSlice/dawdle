from functools import wraps

from flask import abort, request


def expects_json(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            abort(415)
        return view(*args, **kwargs)
    return decorated_function
