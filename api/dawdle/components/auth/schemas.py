from marshmallow import EXCLUDE, Schema, fields, pre_load
from marshmallow.validate import Length

from dawdle.utils.schemas import Limits, trim_string


class SignUpSchema(Schema):

    class Meta:
        unknown = EXCLUDE

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
        trim_string(in_data, "email")
        return in_data


class EmailSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    email = fields.Email(required=True)

    @pre_load
    def normalise(self, in_data, **_):
        trim_string(in_data, "email")
        return in_data


class EmailPasswordSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @pre_load
    def normalise(self, in_data, **_):
        trim_string(in_data, "email")
        return in_data


class PasswordSchema(Schema):

    class Meta:
        unknown = EXCLUDE

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
