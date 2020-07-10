import os

from flask import Flask, abort

from dawdle.utils.errors import build_error_response

__VERSION__ = "v0.1.0"


def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)

    __load_config(app, testing)
    __init_extensions(app)
    __register_blueprints(app)
    __attach_error_handlers(app)

    return app


def __load_config(app, testing):
    app.config.from_object("config.Default")

    app.config.from_pyfile("config.py", silent=True)

    def load_env_var(key):
        return os.environ.get(key, app.config.get(key))

    def load_env_var_bool(key):
        return str(load_env_var(key)).lower() == "true"

    app.config.update({
        "CONTACT_EMAIL": load_env_var("CONTACT_EMAIL"),
        "DEBUG": load_env_var_bool("DEBUG"),
        "ENV": load_env_var("ENV"),
        "JWT_SECRET_KEY": load_env_var("JWT_SECRET_KEY"),
        "MONGODB_HOST": load_env_var("MONGODB_HOST"),
        "SECRET_KEY": load_env_var("SECRET_KEY"),
        "SENDER_EMAIL": load_env_var("SENDER_EMAIL"),
        "SENDGRID_API_KEY": load_env_var("SENDGRID_API_KEY"),
        "SERVER_NAME": load_env_var("SERVER_NAME"),
        "SESSION_COOKIE_DOMAIN": load_env_var("SESSION_COOKIE_DOMAIN"),
    })

    app.config.update({"TESTING": testing})

    if testing:
        app.config.from_object("config.Test")


def __init_extensions(app):
    from dawdle.extensions.jwt import jwt
    jwt.init_app(app)

    from dawdle.extensions.marshmallow import marshmallow
    marshmallow.init_app(app)

    from dawdle.extensions.mongoengine import mongoengine
    mongoengine.init_app(app)

    from dawdle.extensions.sendgrid import sendgrid
    sendgrid.init_app(app)


def __register_blueprints(app):
    from dawdle.components.auth.blueprints import auth_bp
    app.register_blueprint(auth_bp)

    from dawdle.components.contact.blueprints import contact_bp
    app.register_blueprint(contact_bp)

    from dawdle.components.home.blueprints import home_bp
    app.register_blueprint(home_bp)

    from dawdle.components.swagger.blueprints import swagger_bp
    app.register_blueprint(swagger_bp)

    from dawdle.components.users.blueprints import users_bp
    app.register_blueprint(users_bp)


def __attach_error_handlers(app):
    @app.errorhandler(Exception)
    def __handle_exception(_):
        abort(500)

    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(415)
    @app.errorhandler(500)
    def __handle_error(error):
        return build_error_response(error.code, error.name, error.description)
