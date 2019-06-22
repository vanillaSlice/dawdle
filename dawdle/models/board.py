from mongoengine import Document, ObjectIdField, StringField


class Board(Document):

    name = StringField(required=True, min_length=1, max_length=256)
    owner_id = ObjectIdField(required=True)
