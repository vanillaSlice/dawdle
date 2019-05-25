"""
Exports reusable util functions.
"""

from bson.errors import InvalidId
from bson.objectid import ObjectId

def to_ObjectId(value):
    """
    Safely converts a value to an ObjectId.
    """

    try:
        return ObjectId(value)
    except InvalidId:
        return ObjectId(None)
