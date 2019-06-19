from datetime import datetime

from bson.objectid import ObjectId
from flask_login import UserMixin
from mongoengine import BooleanField, DateTimeField, Document, EmailField, ObjectIdField, StringField
from passlib.hash import sha256_crypt

class User(Document, UserMixin):

    active = BooleanField(required=True, default=False)
    auth_id = ObjectIdField(required=True, default=ObjectId, unique=True)
    created = DateTimeField(required=True, default=datetime.utcnow)
    email = EmailField(required=True)
    initials = StringField(required=True, min_length=1, max_length=4)
    last_updated = DateTimeField()
    name = StringField(required=True, min_length=1, max_length=50)
    password = StringField(required=True)

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.auth_id)

    @staticmethod
    def encrypt_password(password):
        return sha256_crypt.hash(password)

    def verify_password(self, password):
        return False if password is None else sha256_crypt.verify(password, self.password)
