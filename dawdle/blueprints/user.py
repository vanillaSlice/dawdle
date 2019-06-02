"""
Exports User blueprint.
"""

from flask import Blueprint, render_template
from flask_login import login_required

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/boards', methods=['GET'])
@login_required
def boards():
    """
    Boards route.
    """

    return render_template('user/boards.html')

@user.route('/settings', methods=['GET'])
@login_required
def settings():
    """
    Settings route.
    """

    return render_template('user/settings.html')
