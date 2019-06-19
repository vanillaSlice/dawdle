from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

home = Blueprint('home', __name__, url_prefix='/')

@home.route('/')
def index_GET():
    if current_user.is_authenticated:
        return redirect(url_for('user.boards_GET'))

    return render_template('home/index.html')
