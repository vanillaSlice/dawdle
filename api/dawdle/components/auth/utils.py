from flask import current_app
from itsdangerous import URLSafeSerializer
from passlib.hash import sha256_crypt

from dawdle.components.user.models import User
from dawdle.extensions.sendgrid import sendgrid, TEMPLATE_IDS
from dawdle.utils import remove_extra_whitespace


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
