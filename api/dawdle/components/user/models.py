from datetime import datetime

from bson.objectid import ObjectId
from mongoengine import (BooleanField, DateTimeField, Document, EmailField,
                         ObjectIdField, ReferenceField, StringField)


class User(Document):

    active = BooleanField(required=True, default=False)
    auth_id = ObjectIdField(required=True, default=ObjectId, unique=True)
    created = DateTimeField(required=True, default=datetime.utcnow)
    email = EmailField(required=True, unique=True)
    initials = StringField(required=True)
    last_updated = DateTimeField()
    name = StringField(required=True)
    password = StringField(required=True)
    updated_by = ReferenceField("self")
