import os

from flask import Flask


def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)

    __load_config(app, testing)

    from dawdle.blueprints import home_bp
    app.register_blueprint(home_bp)

    return app


def __load_config(app, testing):
    app.config.from_object("config.Default")

    app.config.from_pyfile("config.py", silent=True)

    def load_env_var(key):
        return os.environ.get(key, app.config.get(key))

    def load_env_var_bool(key):
        return str(load_env_var(key)).lower() == "true"

    # def load_env_var_int(key):
    #     return int(load_env_var(key))

    app.config.update({
        "DEBUG": load_env_var_bool("DEBUG"),
        "ENV": load_env_var("ENV"),
        "SECRET_KEY": load_env_var("SECRET_KEY"),
        "SERVER_NAME": load_env_var("SERVER_NAME"),
        "SESSION_COOKIE_DOMAIN": load_env_var("SESSION_COOKIE_DOMAIN"),
    })

    app.config.update({"TESTING": testing})

    if testing:
        app.config.from_object("config.Test")
