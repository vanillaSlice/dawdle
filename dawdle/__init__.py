"""
Exports a function to create an instance of the Dawdle app.
"""

import os

from flask import Flask

from dawdle.version import __version__

def create_app(testing=False):
    """
    Creates an instance of the Dawdle app.
    """

    app = Flask(__name__, instance_relative_config=True)

    # load default config
    app.config.from_object('config.Default')

    # load instance config (if present)
    app.config.from_pyfile('config.py', silent=True)

    # load test config (if testing)
    if testing:
        app.config.from_object('config.Test')

    app.config.update({'TESTING': testing})

    # load environment variables (if present)
    app.config.update({
        'DEBUG': os.environ.get('DEBUG', str(app.config.get('DEBUG'))).lower() == 'true',
        'ENV': os.environ.get('ENV', app.config.get('ENV')),
        'SECRET_KEY': os.environ.get('SECRET_KEY', app.config.get('SECRET_KEY')),
        'SERVER_NAME': os.environ.get('SERVER_NAME', app.config.get('SERVER_NAME')),
        'SESSION_COOKIE_DOMAIN':
            os.environ.get('SESSION_COOKIE_DOMAIN', app.config.get('SESSION_COOKIE_DOMAIN')),
    })

    # set version
    app.config.update({'VERSION': __version__})

    @app.route('/')
    def home():
        """
        Home route.
        """
        return 'v{}'.format(app.config['VERSION'])

    return app
