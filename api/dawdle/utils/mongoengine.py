from bson.errors import InvalidId
from bson.objectid import ObjectId


def to_ObjectId(value):
    try:
        return ObjectId(value)
    except InvalidId:
        return ObjectId()
