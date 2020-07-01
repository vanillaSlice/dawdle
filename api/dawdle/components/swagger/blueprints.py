from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

__BASE_URL = "/api"
__DOCS_FOLDER = "../docs"
__TEMPLATE_NAME = "api.yml"

swagger_bp = get_swaggerui_blueprint(
    __BASE_URL,
    f"{__BASE_URL}/{__TEMPLATE_NAME}",
)

swagger_bp.url_prefix = __BASE_URL


@swagger_bp.route(f"/{__TEMPLATE_NAME}")
def template_GET():
    return send_from_directory(__DOCS_FOLDER, __TEMPLATE_NAME)
