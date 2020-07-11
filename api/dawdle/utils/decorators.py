from functools import wraps

from flask import abort, request
from flask_jwt_extended import (get_jwt_claims, verify_fresh_jwt_in_request,
                                verify_jwt_in_request)

from dawdle.components.auth.utils import get_user_by_id


def expects_json(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            abort(415)
        return view(*args, **kwargs)
    return decorated_function


def user_admin_required(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        verify_fresh_jwt_in_request()
        __verify_user_id_matches_claim(**kwargs)
        return view(*args, **kwargs)
    return decorated_function


def user_read_required(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        __verify_user_id_matches_claim(**kwargs)
        return view(*args, **kwargs)
    return decorated_function


def __verify_user_id_matches_claim(**kwargs):
    if kwargs["user_id"] != get_jwt_claims().get("user_id"):
        abort(403)


def user_by_id_required(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        user = get_user_by_id(kwargs["user_id"])
        if not user:
            abort(404)
        kwargs["user"] = user
        return view(*args, **kwargs)
    return decorated_function
