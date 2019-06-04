"""
Exports User blueprint.
"""

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

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

@user.route('/delete')
@login_required
def delete_GET():
    """
    Delete GET route.
    """

    return redirect(url_for('user.settings_GET'))

@user.route('/delete', methods=['POST'])
@login_required
def delete_POST():
    """
    Delete POST route.
    """

    current_user.delete()

    flash('Your account has been deleted.', 'info')

    return redirect(url_for('home.index_GET'))
