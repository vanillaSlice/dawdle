from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Length

from dawdle.models.board import BOARD_TYPES
from dawdle.utils import has_board_create_permission, strip


class CreateBoardForm(FlaskForm):

    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Please enter a board name'),
            Length(
                min=1,
                max=256,
                message='Board name must be between 1 and 256 characters',
            ),
        ],
        filters=[strip],
    )

    owner_id = StringField(
        'Owner Id',
        validators=[
            DataRequired(message='Please enter an owner ID'),
        ],
    )

    type = SelectField(
        'Type',
        choices=[(type.id, type.display_name) for type in BOARD_TYPES],
    )

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        if not has_board_create_permission(self.owner_id.data):
            self.owner_id.errors.append(
                'Not authorised to create board with given owner ID',
            )
            return False

        return True
