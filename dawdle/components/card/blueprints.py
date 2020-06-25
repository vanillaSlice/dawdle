from flask import Blueprint, jsonify, request
from flask_login import current_user

from dawdle.components.board.models import BoardPermission
from dawdle.components.board.utils import board_permissions_required
from dawdle.components.card.forms import (CreateCardForm, DeleteCardForm,
                                          UpdateCardForm)
from dawdle.components.card.models import Card
from dawdle.components.card.utils import card_from_card_id, column_id_from_card
from dawdle.components.column.utils import (board_id_from_column,
                                            column_from_column_id)

card_bp = Blueprint('card', __name__, url_prefix='/card')


@card_bp.route('/', methods=['POST'])
@column_from_column_id
@board_id_from_column
@board_permissions_required(BoardPermission.WRITE)
def index_POST(column, **_):
    form = CreateCardForm(request.form)

    if not form.validate_on_submit():
        return jsonify(form.errors), 400

    card = Card()
    form.populate_obj(card)
    card.column_id = column.id
    card.created_by = current_user.id
    card.save()

    column.cards.append(card)
    column.save()

    return jsonify({
        'card': card,
    }), 201


@card_bp.route('/<card_id>', methods=['POST'])
@card_from_card_id
@column_id_from_card
@column_from_column_id
@board_id_from_column
@board_permissions_required(BoardPermission.WRITE)
def card_update_POST(card, **_):
    form = UpdateCardForm(request.form)

    if not form.validate_on_submit():
        return jsonify(form.errors), 400

    form.populate_obj(card)
    card.save()

    return jsonify({
        'card': card,
    }), 200


@card_bp.route('/<card_id>/delete', methods=['POST'])
@card_from_card_id
@column_id_from_card
@column_from_column_id
@board_id_from_column
@board_permissions_required(BoardPermission.WRITE)
def card_delete_POST(card, card_id, **_):
    form = DeleteCardForm(request.form)

    if not form.validate_on_submit():
        return jsonify(form.errors), 400

    card.delete()

    return jsonify({
        'id': card_id,
    }), 200
