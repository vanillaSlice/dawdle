from datetime import datetime

from bson.objectid import ObjectId
from mongoengine import (BooleanField, DateTimeField, Document, EmailField,
                         ObjectIdField, StringField)


class User(Document):

    active = BooleanField(required=True, default=False)
    auth_id = ObjectIdField(required=True, default=ObjectId, unique=True)
    created = DateTimeField(required=True, default=datetime.utcnow)
    email = EmailField(required=True, unique=True)
    initials = StringField(required=True, min_length=1, max_length=4)
    last_updated = DateTimeField(required=True, default=datetime.utcnow)
    name = StringField(required=True, min_length=1, max_length=50)
    password = StringField(required=True)
