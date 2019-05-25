"""
Exports Auth routes.
"""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_mail import Message
from itsdangerous import URLSafeSerializer

from dawdle.forms.auth import SignUpForm, VerifyResendForm
from dawdle.models.user import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

#
# Utils
#

def send_verification_email(user):
    """
    Sends a verification email to the given user.
    """

    token = URLSafeSerializer(current_app.secret_key).dumps(str(user.id))
    message = Message('Dawdle Verification', recipients=[user.email])
    message.html = render_template('auth/verify-email.html', user=user, token=token)
    current_app.mail.send(message)
    flash('A verification email has been sent to {}. '.format(user.email) +
          'Please verify your account before logging in to Dawdle.', 'info')

#
# Routes
#

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Sign Up route.
    """

    # parse the form
    form = SignUpForm(request.form)

    # render form if GET request
    if request.method == 'GET':
        return render_template('auth/sign-up.html', form=form)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('auth/sign-up.html', form=form), 400

    # save new user
    user = User()
    form.populate_obj(user)
    user.password = User.encrypt_password(form.password.data)
    user.save()

    # send verification email
    send_verification_email(user)

    # redirect to verify resend page
    return redirect(url_for('auth.verify_resend'))

@auth.route('/verify/resend', methods=['GET', 'POST'])
def verify_resend():
    """
    Verify Resend route.
    """

    # parse the form
    form = VerifyResendForm(request.form)

    # render form if GET request
    if request.method == 'GET':
        return render_template('auth/verify-resend.html', form=form)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('auth/verify-resend.html', form=form), 400

    # send verification email
    send_verification_email(form.user)

    # redirect to verify resend page again
    return redirect(url_for('auth.verify_resend'))

@auth.route('/verify/<token>', methods=['GET'])
def verify(token):
    """
    Verify Route.
    """

    return token

@auth.route('/login')
def login():
    """
    Login route.
    """

    return render_template('auth/login.html')
