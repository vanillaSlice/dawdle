"""
Exports Auth forms.
"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, Length

from dawdle.models.user import User

class SignUpForm(FlaskForm):
    """
    Sign Up form.
    """

    name = StringField('Name', validators=[
        DataRequired(message='Please enter a name'),
        Length(min=1, max=50, message='Your name must be between 1 and 50 characters'),
    ])

    email = StringField('Email', validators=[
        DataRequired(message='Please enter an email'),
        Email(message='Please enter a valid email'),
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter a password'),
        Length(min=8, message='Your password must be at least 8 characters'),
    ])

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        if User.objects(email=self.email.data).first():
            self.email.errors.append('There is already an account with this email')
            return False

        return True
