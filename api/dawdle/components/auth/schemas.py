from marshmallow import Schema, fields, pre_load
from marshmallow.validate import Length

from dawdle.utils.schemas import Limits, trim_string


class SignUpSchema(Schema):

    name = fields.Str(
        required=True,
        validate=Length(
            max=Limits.MAX_USER_NAME_LENGTH,
        ),
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=Length(
            min=Limits.MIN_USER_PASSWORD_LENGTH,
            max=Limits.MAX_USER_PASSWORD_LENGTH,
        ),
    )

    @pre_load
    def normalise(self, in_data, **_):
        trim_string(in_data, "name")
        return in_data


class EmailSchema(Schema):

    email = fields.Email(required=True)


class EmailPasswordSchema(Schema):

    email = fields.Email(required=True)
    password = fields.Str(required=True)


class PasswordSchema(Schema):

    password = fields.Str(
        required=True,
        validate=Length(
            min=Limits.MIN_USER_PASSWORD_LENGTH,
            max=Limits.MAX_USER_PASSWORD_LENGTH,
        ),
    )


sign_up_schema = SignUpSchema()
email_schema = EmailSchema()
email_password_schema = EmailPasswordSchema()
password_schema = PasswordSchema()
