from flask_jwt_extended import JWTManager

from dawdle.utils.errors import (build_400_error_response,
                                 build_401_error_response)

jwt = JWTManager()


@jwt.expired_token_loader
def expired_token_loader(_):
    return build_400_error_response(messages={
        "token": [
            "Token expired.",
        ],
    })


@jwt.invalid_token_loader
def invalid_token_loader(_):
    return build_400_error_response(messages={
        "token": [
            "Invalid token.",
        ],
    })


@jwt.needs_fresh_token_loader
def needs_fresh_token_loader():
    return build_400_error_response(messages={
        "token": [
            "Needs fresh token.",
        ],
    })


@jwt.unauthorized_loader
def unauthorized_loader(_):
    return build_401_error_response()
