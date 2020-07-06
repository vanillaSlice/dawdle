from datetime import datetime

from bson.objectid import ObjectId
from flask import current_app
from itsdangerous import BadSignature, URLSafeSerializer
from passlib.hash import sha256_crypt

from dawdle.components.user.models import User
from dawdle.extensions.sendgrid import TEMPLATE_IDS, sendgrid
from dawdle.utils import remove_extra_whitespace
from dawdle.utils.mongoengine import to_ObjectId


def save_new_user(name, email, raw_password):
    user = User()
    user.name = name
    user.initials = create_initials(name)
    user.email = email
    user.password = encrypt_password(raw_password)
    user.save()


def encrypt_password(raw_password):
    return sha256_crypt.hash(raw_password)


def verify_password(user_password, password_provided):
    if not password_provided:
        return False
    return sha256_crypt.verify(password_provided, user_password)


def create_initials(name):
    name_trimmed = remove_extra_whitespace(name)
    return "".join([c[0] for c in name_trimmed.split(" ")])[:4].upper()


def send_verification_email(user):
    sendgrid.send(
        TEMPLATE_IDS["verification"],
        user.email,
        data={
            "name": user.name,
            "token": serialize_verification_token(user),
        },
    )


def serialize_verification_token(user):
    return URLSafeSerializer(current_app.secret_key).dumps(str(user.auth_id))


def get_user_from_token(token):
    auth_id = deserialize_verification_token(token)
    return User.objects(auth_id=auth_id).first()


def deserialize_verification_token(token):
    try:
        auth_id = URLSafeSerializer(current_app.secret_key).loads(token)
        return to_ObjectId(auth_id)
    except BadSignature:
        return ObjectId()


def activate_user(user):
    user.active = True
    user.auth_id = ObjectId()
    user.last_updated = datetime.utcnow()
    user.save()
