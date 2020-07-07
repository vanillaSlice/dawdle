# pylint: disable=no-self-use

from marshmallow import Schema, fields, pre_load
from marshmallow.validate import Length

from dawdle.utils.schemas import trim_string


class SignUpSchema(Schema):

    name = fields.Str(required=True, validate=Length(min=1, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(min=8))

    @pre_load
    def normalise_name(self, in_data, **_):
        trim_string(in_data, "name")
        return in_data


class EmailSchema(Schema):

    email = fields.Email(required=True)


class EmailPasswordSchema(Schema):

    email = fields.Email(required=True)
    password = fields.Str(required=True)


class PasswordSchema(Schema):

    password = fields.Str(required=True, validate=Length(min=8))


sign_up_schema = SignUpSchema()
email_schema = EmailSchema()
email_password_schema = EmailPasswordSchema()
password_schema = PasswordSchema()
