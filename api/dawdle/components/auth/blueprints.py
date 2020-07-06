from flask import Blueprint, request

from dawdle.components.auth.schemas import sign_up_schema
from dawdle.components.auth.utils import save_new_user
from dawdle.components.user.utils import user_exists
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
