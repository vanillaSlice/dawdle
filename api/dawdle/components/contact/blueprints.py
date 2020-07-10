from flask import Blueprint, request

from dawdle.components.contact.schemas import contact_schema
from dawdle.components.contact.utils import send_contact_emails
from dawdle.utils.decorators import expects_json
from dawdle.utils.errors import build_400_error_response

contact_bp = Blueprint("contact", __name__, url_prefix="/api/contact")


@contact_bp.route("/", methods=["POST"])
@expects_json
def index_POST():
    errors = contact_schema.validate(request.json)

    if errors:
        return build_400_error_response(errors)

    parsed_schema = contact_schema.dump(request.json)

    send_contact_emails(
        parsed_schema["email"],
        parsed_schema["subject"],
        parsed_schema["message"],
    )

    return "", 204
