"""
Exports User forms.
"""

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets import PasswordInput

from dawdle.models.user import User

class UpdateAccountDetailsForm(FlaskForm):
    """
    Update Account Details form.
    """

    name = StringField('Name', validators=[
        DataRequired(message='Please enter a name'),
        Length(min=1, max=50, message='Your name must be between 1 and 50 characters'),
    ], filters=[lambda s: ' '.join(s.split())])

    initials = StringField('Initials', validators=[
        DataRequired(message='Please enter initials'),
        Length(min=1, max=4, message='Your initials must be between 1 and 4 characters'),
    ], filters=[lambda s: ' '.join(s.split())])

class UpdateEmailForm(FlaskForm):
    """
    Update Email form.
    """

    email = StringField('Email', validators=[
        DataRequired(message='Please enter an email'),
        Email(message='Please enter a valid email'),
    ])

    password = StringField('Password Confirmation', validators=[
        DataRequired(message='Please enter your password'),
    ], widget=PasswordInput(hide_value=False))

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        if not current_user.verify_password(self.password.data):
            self.password.errors.append('Incorrect password')
            return False

        if current_user.email != self.email.data and User.objects(email=self.email.data).first():
            self.email.errors.append('There is already an account with this email')
            return False

        return True

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

class DeleteUserForm(FlaskForm):
    """
    Delete User form.
    """

    password = StringField('Password Confirmation', validators=[
        DataRequired(message='Please enter your password'),
    ], widget=PasswordInput(hide_value=False))

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        if not current_user.verify_password(self.password.data):
            self.password.errors.append('Incorrect password')
            return False

        return True
