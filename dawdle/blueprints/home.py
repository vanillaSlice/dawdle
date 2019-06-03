"""
Exports Home blueprint.
"""

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

home = Blueprint('home', __name__, url_prefix='/')

@home.route('/')
def index_GET():
    """
    Index GET route.
    """

    # redirect to user's boards page if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('user.boards'))

    # otherwise render home page
    return render_template('home/index.html')
