from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                current_user, jwt_refresh_token_required)

from dawdle.components.auth.schemas import (email_password_schema,
                                            email_schema, sign_up_schema)
from dawdle.components.auth.utils import (activate_user, get_user_from_token,
                                          save_new_user,
                                          send_verification_email,
                                          send_password_reset_email,
                                          verify_password)
from dawdle.components.user.utils import get_user_by_email, user_exists
from dawdle.utils.decorators import expects_json
from dawdle.utils.errors import build_400_error_response

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/sign-up", methods=["POST"])
@expects_json
def sign_up_POST():
    errors = sign_up_schema.validate(request.json)

    if errors:
        return build_400_error_response(errors)

    parsed_schema = sign_up_schema.dump(request.json)

    if user_exists(parsed_schema["email"]):
        return build_400_error_response({
            "email": [
                "There is already an account with this email.",
            ],
        })

    save_new_user(
        parsed_schema["name"],
        parsed_schema["email"],
        parsed_schema["password"],
    )

    return "", 201


@auth_bp.route("/verify", methods=["POST"])
@expects_json
def verify_POST():
    errors = email_schema.validate(request.json)

    if errors:
        return build_400_error_response(errors)

    parsed_schema = email_schema.dump(request.json)

    user = get_user_by_email(parsed_schema["email"])

    if not user:
        return build_400_error_response({
            "email": [
                "There is no account with this email.",
            ],
        })

    if user.active:
        return build_400_error_response({
            "email": [
                "This email has already been verified.",
            ],
        })

    send_verification_email(user)

    return "", 204


@auth_bp.route("/verify/<token>", methods=["GET"])
def verify_GET(token):
    user = get_user_from_token(token)

    if not user:
        return build_400_error_response({
            "token": [
                "Invalid token.",
            ],
        })

    activate_user(user)

    return "", 204


@auth_bp.route("/token", methods=["POST"])
@expects_json
def token_POST():
    errors = email_password_schema.validate(request.json)

    if errors:
        return build_400_error_response(errors)

    parsed_schema = sign_up_schema.dump(request.json)

    user = get_user_by_email(parsed_schema["email"])

    if not user or \
       not verify_password(user.password, parsed_schema["password"]):
        return build_400_error_response({
            "email": [
                "Incorrect email.",
            ],
            "password": [
                "Incorrect password.",
            ],
        })

    if not user.active:
        return build_400_error_response({
            "email": [
                "This email has not been verified.",
            ],
        })

    identity = str(user.auth_id)

    return jsonify(
        access_token=create_access_token(identity=identity, fresh=True),
        refresh_token=create_refresh_token(identity=identity),
    ), 200


@auth_bp.route("/token/refresh", methods=["GET"])
@jwt_refresh_token_required
def token_refresh_GET():
    return jsonify(
        access_token=create_access_token(identity=str(current_user.auth_id)),
    ), 200


@auth_bp.route("/reset-password", methods=["POST"])
@expects_json
def reset_password_POST():
    errors = email_schema.validate(request.json)

    if errors:
        return build_400_error_response(errors)

    parsed_schema = email_schema.dump(request.json)

    user = get_user_by_email(parsed_schema["email"])

    if not user:
        return build_400_error_response({
            "email": [
                "There is no account with this email.",
            ],
        })

    send_password_reset_email(user)

    return "", 204
