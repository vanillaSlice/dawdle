from marshmallow import EXCLUDE, Schema, fields, pre_load
from marshmallow.validate import Length

from dawdle.extensions.marshmallow import Limits, trim_string


class ContactSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    email = fields.Email(required=True)
    subject = fields.Str(
        required=True,
        validate=Length(
            max=Limits.MAX_CONTACT_SUBJECT_LENGTH,
        ),
    )
    message = fields.Str(
        required=True,
        validate=Length(
            max=Limits.MAX_CONTACT_MESSAGE_LENGTH,
        ),
    )

    @pre_load
    def normalise(self, in_data, **_):
        trim_string(in_data, "email")
        trim_string(in_data, "subject")
        trim_string(in_data, "message")
        return in_data


contact_schema = ContactSchema()
