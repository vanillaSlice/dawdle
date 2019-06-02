"""
Exports Support blueprint.
"""

from flask import Blueprint, render_template

support = Blueprint('support', __name__, url_prefix='/support')

@support.route('/')
def index():
    """
    Index route.
    """

    return render_template('support/index.html')
