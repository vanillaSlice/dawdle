from flask import Blueprint, redirect, url_for

home_bp = Blueprint("home", __name__, url_prefix="/")


@home_bp.route("/")
def index_GET():
    return redirect(url_for("swagger_ui.show"))
