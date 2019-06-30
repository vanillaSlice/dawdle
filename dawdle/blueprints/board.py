from flask import Blueprint, jsonify, request, url_for
from flask_login import current_user, login_required

from dawdle.forms.board import CreateBoardForm
from dawdle.models.board import Board
from dawdle.utils import get_owner_from_id, to_ObjectId

board_bp = Blueprint('board', __name__, url_prefix='/board')


@board_bp.route('/', methods=['POST'])
@login_required
def index_POST():
    form = CreateBoardForm(request.form)

    if not form.validate_on_submit():
        return jsonify(form.errors), 400

    board = Board()
    board.created_by = current_user.id
    board.name = form.name.data
    board.owner_id = to_ObjectId(form.owner_id.data)
    board.type = form.type.data
    board.save()

    owner = get_owner_from_id(board.owner_id)
    owner.boards.append(board)
    owner.save()

    return jsonify({
        'id': str(board.id),
        'name': board.name,
        'url': url_for('board.board_GET', board_id=board.id),
    }), 201


@board_bp.route('/<board_id>')
def board_GET(board_id):
    return jsonify(board_id)
