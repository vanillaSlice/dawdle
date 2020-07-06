from dawdle.components.user.models import User


def user_exists(email):
    return get_user_by_email(email) is not None


def get_user_by_email(email):
    return User.objects(email=email).first()
