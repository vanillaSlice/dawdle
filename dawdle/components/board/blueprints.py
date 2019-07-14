from flask import Blueprint, jsonify, render_template, request, url_for
from flask_login import current_user

from dawdle.components.board.forms import CreateBoardForm
from dawdle.components.board.models import Board, BoardPermission, BoardType
from dawdle.components.board.utils import (board_permissions_required,
                                           get_owner_from_id)

board_bp = Blueprint('board', __name__, url_prefix='/board')


@board_bp.route('/', methods=['POST'])
def index_POST():
    if not current_user.is_authenticated:
        return jsonify({
            'error': 'Could not create board because you are not logged in.',
        }), 401

    form = CreateBoardForm(request.form)

    if not form.validate_on_submit():
        return jsonify(form.errors), 400

    owner = get_owner_from_id(form.owner.data)

    board = Board()
    board.created_by = current_user.id
    board.name = form.name.data
    board.owner_id = owner.id
    board.type = BoardType.PERSONAL.id if owner.id == current_user.id \
        else BoardType.TEAM.id
    board.visibility = form.visibility.data
    board.save()

    owner.boards.append(board)
    owner.save()

    return jsonify({
        'id': str(board.id),
        'url': url_for('board.board_GET', board_id=board.id),
    }), 201


@board_bp.route('/<board_id>')
@board_permissions_required(BoardPermission.READ)
def board_GET(board, permissions, **_):
    return render_template(
        'board/index.html',
        board=board,
        permissions=permissions,
    )