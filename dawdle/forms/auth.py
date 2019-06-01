"""
Exports Auth forms.
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets import PasswordInput

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

    password = StringField('Password', validators=[
        DataRequired(message='Please enter a password'),
        Length(min=8, message='Your password must be at least 8 characters'),
    ], widget=PasswordInput(hide_value=False))

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        if User.objects(email=self.email.data).first():
            self.email.errors.append('There is already an account with this email')
            return False

        return True

class VerifyResendForm(FlaskForm):
    """
    Verify Resend form.
    """

    email = StringField('Email', validators=[
        DataRequired(message='Please enter an email'),
        Email(message='Please enter a valid email'),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        self.user = User.objects(email=self.email.data).first()

        if self.user is None:
            self.email.errors.append('There is no account with this email')
            return False

        if self.user.is_active:
            self.email.errors.append('This account has already been verified')
            return False

        return True

class LoginForm(FlaskForm):
    """
    Login form.
    """

    email = StringField('Email', validators=[
        DataRequired(message='Please enter an email'),
        Email(message='Please enter a valid email'),
    ])

    password = StringField('Password', validators=[
        DataRequired(message='Please enter a password'),
    ], widget=PasswordInput(hide_value=False))

    remember_me = BooleanField('Remember Me')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        self.user = User.objects(email=self.email.data).first()

        if self.user is None or not self.user.verify_password(self.password.data):
            self.email.errors.append('Incorrect email')
            self.password.errors.append('Incorrect password')
            return False

        if not self.user.is_active:
            self.email.errors.append('Please verify your account before logging in')
            return False

        return True

class ResetPasswordRequestForm(FlaskForm):
    """
    Reset Password Request form.
    """

    email = StringField('Email', validators=[
        DataRequired(message='Please enter an email'),
        Email(message='Please enter a valid email'),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        self.user = User.objects(email=self.email.data).first()

        if self.user is None:
            self.email.errors.append('There is no account with this email')
            return False

        return True

class ResetPasswordForm(FlaskForm):
    """
    Reset Password form.
    """

    password = StringField('Password', validators=[
        DataRequired(message='Please enter a password'),
        Length(min=8, message='Your password must be at least 8 characters'),
    ], widget=PasswordInput(hide_value=False))

    confirmation = StringField('Confirmation', validators=[
        DataRequired(message='Please enter password confirmation'),
        EqualTo('password', message='Password and confirmation must match'),
    ], widget=PasswordInput(hide_value=False))
