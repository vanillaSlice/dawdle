from urllib.parse import urljoin, urlparse

from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import request


def to_ObjectId(value):
    try:
        return ObjectId(value)
    except InvalidId:
        return ObjectId()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def safely_delete_documents(documents):
    for document in documents:
        safely_delete_document(document)


def safely_delete_document(document):
    try:
        document.delete()
    except Exception:
        pass
