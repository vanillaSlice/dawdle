from passlib.hash import sha256_crypt

from dawdle.components.auth.utils import encrypt_password
from dawdle.components.user.models import User


def user_exists(email):
    return get_user_by_email(email) is not None


def save_new_user(name, email, raw_password):
    user = User()
    user.name = name
    user.email = email
    user.password = encrypt_password(raw_password)
    user.initials = create_initials(name)
    user.save()


def create_initials(name):
    return "".join([c[0].upper() for c in name.split(" ")])[:4]


def get_user_by_email(email):
    return User.objects(email=email).first()
