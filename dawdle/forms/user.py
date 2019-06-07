"""
Exports User forms.
"""

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import PasswordInput

class UpdatePasswordForm(FlaskForm):
    """
    Update Password form.
    """

    current_password = StringField('Current Password', validators=[
        DataRequired(message='Please enter your current password'),
    ], widget=PasswordInput(hide_value=False))

    new_password = StringField('New Password', validators=[
        DataRequired(message='Please enter a new password'),
        Length(min=8, message='Your new password must be at least 8 characters'),
    ], widget=PasswordInput(hide_value=False))

    confirmation = StringField('Confirmation', validators=[
        DataRequired(message='Please enter new password confirmation'),
        EqualTo('new_password', message='New password and confirmation must match'),
    ], widget=PasswordInput(hide_value=False))

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        if not current_user.verify_password(self.current_password.data):
            self.current_password.errors.append('Incorrect current password')
            return False

        return True
