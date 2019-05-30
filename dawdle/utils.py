"""
Exports reusable util functions.
"""

from urllib.parse import urljoin, urlparse

from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import request

def to_ObjectId(value):
    """
    Safely converts a value to an ObjectId.
    """

    try:
        return ObjectId(value)
    except InvalidId:
        return ObjectId(None)

def is_safe_url(target):
    """
    Ensures that a redirect target will lead to the same server.
    """

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
