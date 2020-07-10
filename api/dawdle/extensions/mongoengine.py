from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask_mongoengine import MongoEngine

mongoengine = MongoEngine()


def to_ObjectId(value):
    try:
        return ObjectId(value)
    except InvalidId:
        return ObjectId()
