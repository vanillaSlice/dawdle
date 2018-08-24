"""
Exports a function to create an instance of the Dawdle app.
"""

from flask import Flask

def create_app():
    """
    Creates an instance of the Dawdle app.
    """

    app = Flask(__name__)

    @app.route('/')
    def home():
        """
        Home route.
        """
        return 'Working on it'

    return app
