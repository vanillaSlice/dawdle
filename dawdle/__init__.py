import os

from flask import Flask, render_template

from dawdle.blueprints.auth import auth as auth_blueprint
from dawdle.blueprints.contact import contact as contact_blueprint
from dawdle.blueprints.home import home as home_blueprint
from dawdle.blueprints.user import user as user_blueprint
from dawdle.extensions.assets import assets as assets_extension
from dawdle.extensions.login import login_manager as login_manager_extension
from dawdle.extensions.mail import mail as mail_extension
from dawdle.extensions.mongoengine import mongoengine as mongoengine_extension

version = '0.1.0'

def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)

    _load_config(app, testing)
    _init_extensions(app)
    _register_blueprints(app)
    _attach_error_handlers(app)
    _disable_caching_when_debugging(app)
    _disable_strict_trailing_slashes(app)

    return app

def _load_config(app, testing):
    conf = app.config

    conf.from_object('config.Default')

    conf.from_pyfile('config.py', silent=True)

    if testing:
        conf.from_object('config.Test')

    env = os.environ
    conf.update({
        'CONTACT_EMAIL': env.get('CONTACT_EMAIL', conf.get('CONTACT_EMAIL')),
        'DEBUG': env.get('DEBUG', str(conf.get('DEBUG'))).lower() == 'true',
        'ENV': env.get('ENV', conf.get('ENV')),
        'MAIL_DEFAULT_SENDER': env.get('MAIL_DEFAULT_SENDER', conf.get('MAIL_DEFAULT_SENDER')),
        'MAIL_PASSWORD': env.get('MAIL_PASSWORD', conf.get('MAIL_PASSWORD')),
        'MAIL_PORT': int(env.get('MAIL_PORT', conf.get('MAIL_PORT'))),
        'MAIL_SERVER': env.get('MAIL_SERVER', conf.get('MAIL_SERVER')),
        'MAIL_SUPPRESS_SEND': env.get('MAIL_SUPPRESS_SEND', str(conf.get('MAIL_SUPPRESS_SEND'))).lower() == 'true',
        'MAIL_USE_SSL': env.get('MAIL_USE_SSL', str(conf.get('MAIL_USE_SSL'))).lower() == 'true',
        'MAIL_USE_TLS': env.get('MAIL_USE_TLS', str(conf.get('MAIL_USE_TLS'))).lower() == 'true',
        'MAIL_USERNAME': env.get('MAIL_USERNAME', conf.get('MAIL_USERNAME')),
        'MONGODB_DB': env.get('MONGODB_DB', conf.get('MONGODB_DB')),
        'MONGODB_HOST': env.get('MONGODB_HOST', conf.get('MONGODB_HOST')),
        'MONGODB_PASSWORD': env.get('MONGODB_PASSWORD', conf.get('MONGODB_PASSWORD')),
        'MONGODB_PORT': int(env.get('MONGODB_PORT', conf.get('MONGODB_PORT'))),
        'MONGODB_USERNAME': env.get('MONGODB_USERNAME', conf.get('MONGODB_USERNAME')),
        'SECRET_KEY': env.get('SECRET_KEY', conf.get('SECRET_KEY')),
        'SERVER_NAME': env.get('SERVER_NAME', conf.get('SERVER_NAME')),
        'SESSION_COOKIE_DOMAIN': env.get('SESSION_COOKIE_DOMAIN', conf.get('SESSION_COOKIE_DOMAIN')),
        'TESTING': testing,
        'VERSION': version,
        'WTF_CSRF_ENABLED': env.get('WTF_CSRF_ENABLED', str(conf.get('WTF_CSRF_ENABLED'))).lower() == 'true',
    })

def _init_extensions(app):
    assets_extension.init_app(app)
    login_manager_extension.init_app(app)
    mail_extension.init_app(app)
    mongoengine_extension.init_app(app)

def _register_blueprints(app):
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(contact_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(user_blueprint)

def _attach_error_handlers(app):
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def handle_error(error):
        return render_template('error/{}.html'.format(error.code), error=error), error.code

def _disable_caching_when_debugging(app):
    if app.debug:
        @app.after_request
        def after_request(response):
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Expires'] = 0
            response.headers['Pragma'] = 'no-cache'
            return response

def _disable_strict_trailing_slashes(app):
    app.url_map.strict_slashes = False
