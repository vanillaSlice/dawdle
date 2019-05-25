"""
Exports User routes.
"""

from flask import Blueprint, render_template
from flask_login import login_required

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<user_id>/boards', methods=['GET'])
@login_required
def boards(user_id):
    """
    Boards route.
    """

    return render_template('user/boards.html')
