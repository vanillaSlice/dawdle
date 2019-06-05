"""
Exports Contact blueprint.
"""

from flask import Blueprint, render_template

contact = Blueprint('contact', __name__, url_prefix='/contact')

@contact.route('/')
def index_GET():
    """
    Index GET route.
    """

    return render_template('contact/index.html')
