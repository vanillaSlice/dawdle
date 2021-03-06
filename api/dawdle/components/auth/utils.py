from datetime import datetime

from bson.objectid import ObjectId
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from itsdangerous import (BadSignature, TimedJSONWebSignatureSerializer,
                          URLSafeSerializer)
from passlib.hash import sha256_crypt

from dawdle.components.users.models import User
from dawdle.extensions.marshmallow import Limits
from dawdle.extensions.mongoengine import to_ObjectId
from dawdle.extensions.sendgrid import TemplateIds, sendgrid
from dawdle.utils import remove_extra_whitespace

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
        {
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
    return user.save()


def create_fresh_user_access_token(user):
    return create_user_access_token(user, fresh=True)


def create_user_access_token(user, fresh=False):
    return create_access_token(
        str(user.auth_id),
        fresh=fresh,
        user_claims={
            "user_id": str(user.id),
        },
    )


def create_user_refresh_token(user):
    return create_refresh_token(str(user.auth_id))


def send_password_reset_email(user):
    sendgrid.send(
        TemplateIds.PASSWORD_RESET,
        user.email,
        {
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
    return user.save()


def get_user_by_id(user_id):
    return User.objects(id=user_id).first()


def delete_user(user):
    user.delete()
    return user


def send_deletion_email(user):
    sendgrid.send(
        TemplateIds.ACCOUNT_DELETION,
        user.email,
        {"name": user.name},
    )


def update_user_email(user, email):
    user.active = False
    user.auth_id = ObjectId()
    user.email = email
    user.last_updated = datetime.utcnow()
    user.updated_by = user
    return user.save()
