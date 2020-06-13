from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField
from wtforms.validators import DataRequired, Length

from dawdle.components.board.models import BOARD_VISIBILITIES


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
        filters=[lambda s: s.strip()],
    )

    owner = SelectField(
        'Owner',
        validators=[
            DataRequired(message='Please select board owner'),
        ],
    )

    visibility = SelectField(
        'Visibility',
        choices=[(v.id, v.display_name) for v in BOARD_VISIBILITIES],
        validators=[
            DataRequired(message='Please select board visibility'),
        ],
    )

    def __init__(self, *args, **kwargs):
        super(CreateBoardForm, self).__init__(*args, **kwargs)
        # TODO add teams to choices # pylint: disable=fixme
        self.owner.choices = [(str(current_user.id), 'Me')]


class DeleteBoardForm(FlaskForm):

    delete_board_path = HiddenField()
