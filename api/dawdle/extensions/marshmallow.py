from flask_marshmallow import Marshmallow

from dawdle.utils import remove_extra_whitespace

marshmallow = Marshmallow()


class Limits:

    MAX_USER_INITIALS_LENGTH = 4
    MAX_USER_NAME_LENGTH = 50
    MIN_USER_PASSWORD_LENGTH = 8
    MAX_USER_PASSWORD_LENGTH = 128


def trim_string(in_data, key):
    value = in_data.get(key)

    if not isinstance(value, str):
        return

    trimmed = remove_extra_whitespace(value)

    if not trimmed:
        del in_data[key]
        return

    in_data[key] = trimmed
