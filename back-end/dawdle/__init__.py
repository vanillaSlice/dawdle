from flask import Blueprint, Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(Blueprint("home", __name__, url_prefix="/"))

    return app


@home_bp.route("/")
def index_GET():
    return "Hello Dawdle!"
