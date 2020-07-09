from datetime import datetime

from bson.objectid import ObjectId
from flask import current_app
from itsdangerous import (BadSignature, TimedJSONWebSignatureSerializer,
                          URLSafeSerializer)
from passlib.hash import sha256_crypt

from dawdle.components.user.models import User
from dawdle.extensions.sendgrid import TemplateIds, sendgrid
from dawdle.utils import remove_extra_whitespace
from dawdle.utils.mongoengine import to_ObjectId
from dawdle.utils.schemas import Limits

_PASSWORD_RESET_TOKEN_EXPIRATION = 900


def get_user_by_email(email):
    return User.objects(email=email).first()


def save_new_user(name, email, raw_password):
    user = User()
    user.name = name
    user.initials = __create_initials(name)
    user.email = email
    user.password = encrypt_password(raw_password)
    return user.save()


def __create_initials(name):
    name_trimmed = remove_extra_whitespace(name)
    split = "".join([c[0] for c in name_trimmed.split(" ")])
    return split[:Limits.MAX_USER_INITIALS_LENGTH].upper()


def encrypt_password(raw_password):
    return sha256_crypt.hash(raw_password)


def verify_password(user_password, password_provided):
    if not password_provided:
        return False
    return sha256_crypt.verify(password_provided, user_password)


def send_verification_email(user):
    sendgrid.send(
        TemplateIds.VERIFICATION,
        user.email,
        data={
            "name": user.name,
            "token": _serialize_verification_token(user),
        },
    )


def _serialize_verification_token(data):
    auth_id = str(data.auth_id) if isinstance(data, User) else data
    return URLSafeSerializer(current_app.secret_key).dumps(auth_id)


def get_user_from_verification_token(token):
    auth_id = __deserialize_verification_token(token)
    return get_user_by_auth_id(auth_id)


def __deserialize_verification_token(token):
    try:
        auth_id = URLSafeSerializer(current_app.secret_key).loads(token)
        return to_ObjectId(auth_id)
    except BadSignature:
        return ObjectId()


def get_user_by_auth_id(auth_id):
    return User.objects(auth_id=to_ObjectId(auth_id)).first()


def activate_user(user):
    user.active = True
    user.auth_id = ObjectId()
    user.last_updated = datetime.utcnow()
    user.updated_by = user
    user.save()


def send_password_reset_email(user):
    sendgrid.send(
        TemplateIds.PASSWORD_RESET,
        user.email,
        data={
            "name": user.name,
            "token": _serialize_password_reset_token(user),
            "expiration": _PASSWORD_RESET_TOKEN_EXPIRATION,
        },
    )


def _serialize_password_reset_token(data, **kwargs):
    auth_id = str(data.auth_id) if isinstance(data, User) else data
    expires_in = kwargs.get(
        "expires_in",
        _PASSWORD_RESET_TOKEN_EXPIRATION,
    )
    return TimedJSONWebSignatureSerializer(
        current_app.secret_key,
        expires_in=expires_in,
    ).dumps(auth_id).decode()


def get_user_from_password_reset_token(token):
    auth_id = __deserialize_password_reset_token(token)
    return get_user_by_auth_id(auth_id)


def __deserialize_password_reset_token(token, **kwargs):
    expires_in = kwargs.get(
        "expires_in",
        _PASSWORD_RESET_TOKEN_EXPIRATION,
    )
    try:
        auth_id = TimedJSONWebSignatureSerializer(
            current_app.secret_key,
            expires_in=expires_in,
        ).loads(token)
        return to_ObjectId(auth_id)
    except BadSignature:
        return ObjectId()


def update_user_password(user, password):
    user.auth_id = ObjectId()
    user.last_updated = datetime.utcnow()
    user.password = encrypt_password(password)
    user.updated_by = user
    user.save()


def get_user_by_id(user_id):
    return User.objects(id=user_id).first()
