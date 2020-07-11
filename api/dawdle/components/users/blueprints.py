from flask import Blueprint, jsonify

from dawdle.components.users.schemas import user_schema
from dawdle.utils.decorators import user_read_required, user_by_id_required

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/<user_id>/info", methods=["GET"])
@user_read_required
@user_by_id_required
def users_user_info_GET(user, **_):
    return jsonify(user_schema.dump(user)), 200
