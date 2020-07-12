from flask import jsonify
from werkzeug import exceptions
from werkzeug.http import HTTP_STATUS_CODES


def build_error_response(status, name, description, messages=None):
    messages = messages if messages else {}
    response_json = jsonify({
        "status": status,
        "name": name,
        "description": description,
        "messages": messages,
    })
    return response_json, status


def build_error_response_from_exception(exception, messages=None):
    return build_error_response(
        exception.code,
        HTTP_STATUS_CODES[exception.code],
        exception.description,
        messages,
    )


def build_400_error_response(messages=None):
    return build_error_response_from_exception(exceptions.BadRequest, messages)


def build_401_error_response(messages=None):
    return build_error_response_from_exception(
        exceptions.Unauthorized,
        messages,
    )
