"""
Exports a function to create an instance of the Dawdle app.
"""

import os

from flask import Flask
from flask_mongoengine import MongoEngine

from dawdle.version import __version__

mongoengine = MongoEngine()

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
        'MONGODB_DB': os.environ.get('MONGODB_DB', app.config.get('MONGODB_DB')),
        'MONGODB_HOST': os.environ.get('MONGODB_HOST', app.config.get('MONGODB_HOST')),
        'MONGODB_PASSWORD': os.environ.get('MONGODB_PASSWORD', app.config.get('MONGODB_PASSWORD')),
        'MONGODB_PORT': os.environ.get('MONGODB_PORT', app.config.get('MONGODB_PORT')),
        'MONGODB_USERNAME': os.environ.get('MONGODB_USERNAME', app.config.get('MONGODB_USERNAME')),
        'SECRET_KEY': os.environ.get('SECRET_KEY', app.config.get('SECRET_KEY')),
        'SERVER_NAME': os.environ.get('SERVER_NAME', app.config.get('SERVER_NAME')),
        'SESSION_COOKIE_DOMAIN':
            os.environ.get('SESSION_COOKIE_DOMAIN', app.config.get('SESSION_COOKIE_DOMAIN')),
    })

    # set version
    app.config.update({'VERSION': __version__})

    # init extensions
    mongoengine.init_app(app)

    @app.route('/')
    def home():
        """
        Home route.
        """
        return 'v{}'.format(app.config['VERSION'])

    return app
