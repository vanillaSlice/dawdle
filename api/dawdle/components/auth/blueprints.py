from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import (fresh_jwt_required, get_jwt_claims,
                                get_jwt_identity, jwt_refresh_token_required)

from dawdle.components.auth.schemas import (email_password_schema,
                                            email_schema, password_schema,
                                            sign_up_schema)
from dawdle.components.auth.utils import (activate_user,
                                          create_fresh_user_access_token,
                                          create_user_access_token,
                                          create_user_refresh_token,
                                          get_user_by_auth_id,
                                          get_user_by_email, get_user_by_id,
                                          get_user_from_password_reset_token,
                                          get_user_from_verification_token,
                                          save_new_user,
                                          send_password_reset_email,
                                          send_verification_email,
                                          update_user_password,
                                          verify_password)
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

    if get_user_by_email(parsed_schema["email"]):
        return build_400_error_response({
            "email": [
                "There is already an account with this email.",
            ],
        })

    user = save_new_user(
        parsed_schema["name"],
        parsed_schema["email"],
        parsed_schema["password"],
    )

    send_verification_email(user)

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
        abort(404)

    if user.active:
        return build_400_error_response({
            "email": [
                "This email has already been verified.",
            ],
        })

    send_verification_email(user)

    return "", 204


@auth_bp.route("/verify/<token>", methods=["POST"])
def verify_token_POST(token):
    user = get_user_from_verification_token(token)

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

    if not user:
        abort(404)

    if not verify_password(user.password, parsed_schema["password"]):
        return build_400_error_response({
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

    return jsonify(
        access_token=create_fresh_user_access_token(user),
        refresh_token=create_user_refresh_token(user),
        user_id=str(user.id),
    ), 200


@auth_bp.route("/token/refresh", methods=["GET"])
@jwt_refresh_token_required
def token_refresh_GET():
    user = get_user_by_auth_id(get_jwt_identity())

    if not user:
        return build_400_error_response({
            "token": [
                "Invalid token.",
            ],
        })

    return jsonify(
        access_token=create_user_access_token(user),
        user_id=str(user.id),
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
        abort(404)

    send_password_reset_email(user)

    return "", 204


@auth_bp.route("/reset-password/<token>", methods=["POST"])
@expects_json
def reset_password_token_POST(token):
    errors = password_schema.validate(request.json)

    if errors:
        return build_400_error_response(errors)

    user = get_user_from_password_reset_token(token)

    if not user:
        return build_400_error_response({
            "token": [
                "Invalid token.",
            ],
        })

    parsed_schema = password_schema.dump(request.json)

    update_user_password(user, parsed_schema["password"])

    return "", 204


@auth_bp.route("/users/<user_id>/password", methods=["POST"])
@expects_json
@fresh_jwt_required
def users_user_password_POST(user_id):
    if user_id != get_jwt_claims().get("user_id"):
        abort(403)

    errors = password_schema.validate(request.json)

    if errors:
        return build_400_error_response(errors)

    parsed_schema = password_schema.dump(request.json)

    user = get_user_by_id(user_id)

    if not user:
        abort(404)

    update_user_password(user, parsed_schema["password"])

    return "", 204
