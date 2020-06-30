from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.update({"SERVER_NAME": "127.0.0.1:5000"})

    from dawdle.blueprints import home_bp
    app.register_blueprint(home_bp)

    return app
