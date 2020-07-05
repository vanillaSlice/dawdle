from flask import jsonify


def build_error_response(status, name, description, messages=None):
    messages = messages if messages else {}
    response_json = jsonify({
        "status": status,
        "name": name,
        "description": description,
        "messages": messages,
    })
    return response_json, status


def build_400_error_response(messages=None):
    return build_error_response(
        400,
        "Bad Request",
        "The browser (or proxy) sent a request that this server could not "
        "understand.",
        messages,
    )
