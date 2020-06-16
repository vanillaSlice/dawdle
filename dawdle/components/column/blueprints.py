from flask import Blueprint, jsonify, request
from flask_login import current_user

from dawdle.components.board.models import BoardPermission
from dawdle.components.board.utils import board_permissions_required
from dawdle.components.column.forms import CreateColumnForm, DeleteColumnForm
from dawdle.components.column.models import Column
from dawdle.components.column.utils import board_id_from_column_id
from dawdle.utils import to_ObjectId

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
        'column': column,
    }), 201


@column_bp.route('/<column_id>/delete', methods=['POST'])
@board_id_from_column_id
@board_permissions_required(BoardPermission.WRITE)
def column_delete_POST(column_id, **_):
    form = DeleteColumnForm(request.form)

    if not form.validate_on_submit():
        return jsonify(form.errors), 400

    column = Column.objects(id=to_ObjectId(column_id))
    column.delete()

    return jsonify({
        'id': column_id,
    }), 200
