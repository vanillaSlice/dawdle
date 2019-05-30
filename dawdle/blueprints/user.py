"""
Exports User blueprint.
"""

from flask import abort, Blueprint, render_template
from flask_login import current_user, login_required

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<user_id>/boards', methods=['GET'])
@login_required
def boards(user_id):
    """
    Boards route.
    """

    if str(current_user.id) != user_id:
        return abort(403)

    return render_template('user/boards.html')
