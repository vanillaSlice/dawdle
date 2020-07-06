from flask_jwt_extended import JWTManager

from dawdle.components.auth.utils import get_user_from_auth_id
from dawdle.utils.errors import (build_400_error_response,
                                 build_401_error_response)

jwt = JWTManager()


@jwt.expired_token_loader
def expired_token_loader(_):
    return build_400_error_response(messages={
        "token": "Token expired.",
    })


@jwt.invalid_token_loader
@jwt.user_loader_error_loader
def invalid_token_loader(_):
    return build_400_error_response(messages={
        "token": "Invalid token.",
    })


@jwt.unauthorized_loader
def unauthorized_loader(_):
    return build_401_error_response()


@jwt.user_loader_callback_loader
def user_loader_callback_loader(identity):
    return get_user_from_auth_id(identity)
