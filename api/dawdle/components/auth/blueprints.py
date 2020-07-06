from flask import Blueprint, request

from dawdle.components.auth.schemas import sign_up_schema, verify_schema
from dawdle.components.auth.utils import save_new_user, send_verification_email
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

    user_schema = sign_up_schema.dump(request.json)

    if user_exists(user_schema["email"]):
        return build_400_error_response({
            "email": [
                "There is already an account with this email.",
            ],
        })

    save_new_user(
        user_schema["name"],
        user_schema["email"],
        user_schema["password"],
    )

    return "", 201


@auth_bp.route("/verify", methods=["POST"])
@expects_json
def verify_POST():
    errors = verify_schema.validate(request.json)

    if errors:
        return build_400_error_response(errors)

    email_schema = verify_schema.dump(request.json)

    user = get_user_by_email(email_schema["email"])

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
