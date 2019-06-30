from collections import namedtuple
from datetime import datetime

from mongoengine import DateTimeField, Document, ObjectIdField, StringField


_board_type = namedtuple('BoardType', 'id, display_name')


class BoardType:
    PERSONAL = _board_type('personal', 'Personal')


BOARD_TYPES = [BoardType.PERSONAL]


class Board(Document):

    created = DateTimeField(required=True, default=datetime.utcnow)
    created_by = ObjectIdField(required=True)
    name = StringField(required=True, min_length=1, max_length=256)
    owner_id = ObjectIdField(required=True)
    type = StringField(required=True)
