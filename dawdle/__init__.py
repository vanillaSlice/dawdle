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
    config = app.config
    environ = os.environ
    logger = app.logger

    logger.setLevel('INFO')

    logger.info('Loading default config')
    config.from_object('config.Default')

    logger.info('Loading instance config')
    config.from_pyfile('config.py', silent=True)

    if testing:
        logger.info('Loading test config')
        config.from_object('config.Test')

    logger.info('Loading environment variables')
    config.update({
        'DEBUG': environ.get('DEBUG', str(config.get('DEBUG'))).lower() == 'true',
        'ENV': environ.get('ENV', config.get('ENV')),
        'MONGODB_DB': environ.get('MONGODB_DB', config.get('MONGODB_DB')),
        'MONGODB_HOST': environ.get('MONGODB_HOST', config.get('MONGODB_HOST')),
        'MONGODB_PASSWORD': environ.get('MONGODB_PASSWORD', config.get('MONGODB_PASSWORD')),
        'MONGODB_PORT': environ.get('MONGODB_PORT', config.get('MONGODB_PORT')),
        'MONGODB_USERNAME': environ.get('MONGODB_USERNAME', config.get('MONGODB_USERNAME')),
        'SECRET_KEY': environ.get('SECRET_KEY', config.get('SECRET_KEY')),
        'SERVER_NAME': environ.get('SERVER_NAME', config.get('SERVER_NAME')),
        'SESSION_COOKIE_DOMAIN': environ.get('SESSION_COOKIE_DOMAIN', config.get('SESSION_COOKIE_DOMAIN')),
    })

    config.update({
        'TESTING': testing,
        'VERSION': __version__,
    })

    logger.info('Initialising extensions')
    mongoengine.init_app(app)

    @app.route('/')
    def home():
        """
        Home route.
        """
        return 'v{}'.format(config['VERSION'])

    return app
