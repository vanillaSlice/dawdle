from marshmallow import EXCLUDE, Schema, fields

from dawdle.extensions.marshmallow import DATETIME_FORMAT


class UserSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    created = fields.DateTime(format=DATETIME_FORMAT)
    email = fields.Email()
    initials = fields.Str()
    name = fields.Str()


user_schema = UserSchema()
