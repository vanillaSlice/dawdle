from flask import Blueprint, jsonify, request
from flask_login import current_user

from dawdle.components.board.models import BoardPermission
from dawdle.components.board.utils import board_permissions_required
from dawdle.components.column.forms import CreateColumnForm
from dawdle.components.column.models import Column

column_bp = Blueprint('column', __name__, url_prefix='/column')


@column_bp.route('/', methods=['POST'])
@board_permissions_required(BoardPermission.WRITE)
def index_POST(board, **_):
    form = CreateColumnForm(request.form)

    if not form.validate_on_submit():
        return jsonify(form.errors), 400

    column = Column()
    form.populate_obj(column)
    column.board_id = board.id
    column.created_by = current_user.id
    column.save()

    board.columns.append(column)
    board.save()

    return jsonify({
        'id': str(column.id),
    }), 201
