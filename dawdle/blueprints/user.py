"""
Exports User blueprint.
"""

from flask import Blueprint, render_template
from flask_login import login_required

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/boards')
@login_required
def boards_GET():
    """
    Boards GET route.
    """

    return render_template('user/boards.html')

@user.route('/settings')
@login_required
def settings_GET():
    """
    Settings GET route.
    """

    return render_template('user/settings.html')
