from flask import Blueprint, abort, jsonify
from flask_jwt_extended import get_jwt_claims, jwt_required

from dawdle.components.auth.utils import get_user_by_id
from dawdle.components.users.schemas import user_schema

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/<user_id>/info", methods=["GET"])
@jwt_required
def users_user_info_GET(user_id):
    if user_id != get_jwt_claims().get("user_id"):
        abort(403)

    user = get_user_by_id(user_id)

    if not user:
        abort(404)

    return jsonify(user_schema.dump(user)), 200
