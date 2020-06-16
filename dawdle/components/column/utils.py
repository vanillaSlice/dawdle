from functools import wraps

from flask import abort

from dawdle.components.column.models import Column
from dawdle.utils import to_ObjectId


def board_id_from_column_id(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        column_id = kwargs['column_id']

        column = Column.objects(id=to_ObjectId(column_id)).first()

        if not column:
            abort(404)

        kwargs['board_id'] = str(column.board_id)
        kwargs['column'] = column

        return func(*args, **kwargs)
    return decorated_function
