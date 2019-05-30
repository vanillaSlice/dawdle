"""
Exports Auth routes.
"""

from datetime import datetime

from bson.objectid import ObjectId
from flask import abort, Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from flask_mail import Message
from itsdangerous import BadSignature, TimedJSONWebSignatureSerializer, URLSafeSerializer

from dawdle.extensions.mail import mail
from dawdle.forms.auth import LoginForm, ResetPasswordForm, ResetPasswordRequestForm, SignUpForm, VerifyResendForm
from dawdle.models.user import User
from dawdle.utils import is_safe_url, to_ObjectId

auth = Blueprint('auth', __name__, url_prefix='/auth')

#
# Utils
#

def send_verification_email(user):
    """
    Sends a verification email to the given user and returns true or false depending
    on whether this was successful.
    """

    token = URLSafeSerializer(current_app.secret_key).dumps(str(user.auth_id))
    message = Message('Dawdle Verification', recipients=[user.email])
    message.html = render_template('auth/verify-email.html', user=user, token=token)
    try:
        mail.send(message)
        flash('A verification email has been sent to {}. '.format(user.email) +
              'Please verify your account before logging in to Dawdle.', 'success')
        return True
    except:
        flash('Could not send a verification email to {}. '.format(user.email) +
              'Please try again.', 'danger')
        return False

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
    return redirect(url_for('auth.verify_resend', email=form.email.data))

@auth.route('/verify/resend', methods=['GET', 'POST'])
def verify_resend():
    """
    Verify Resend route.
    """

    # parse the form
    form = VerifyResendForm(request.form, email=request.args.get('email'))

    # render form if GET request
    if request.method == 'GET':
        return render_template('auth/verify-resend.html', form=form)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('auth/verify-resend.html', form=form), 400

    # send verification email
    sent_email = send_verification_email(form.user)
    status_code = 200 if sent_email else 500

    # render form again
    return render_template('auth/verify-resend.html', form=form), status_code

@auth.route('/verify/<token>', methods=['GET'])
def verify(token):
    """
    Verify route.
    """

    # make sure we have a valid token
    try:
        auth_id = URLSafeSerializer(current_app.secret_key).loads(token)
    except BadSignature:
        return abort(404)

    # make sure the user with the given auth id exists
    user = User.objects(auth_id=to_ObjectId(auth_id)).first()
    if user is None:
        abort(404)

    # activate the user (making sure to update the auth id and last updated)
    user.active = True
    user.auth_id = ObjectId()
    user.last_updated = datetime.utcnow()
    user.save()

    # login the new user
    login_user(user, remember=True)

    # notify the user
    flash('Your user registration was successful.', 'success')

    # redirect to user's boards page
    return redirect(url_for('user.boards', user_id=str(user.id)))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route.
    """

    # parse the form
    form = LoginForm(request.form)

    # render form if GET request
    if request.method == 'GET':
        return render_template('auth/login.html', form=form)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('auth/login.html', form=form), 400

    # login the user
    user = form.user
    login_user(user, remember=form.remember_me.data)

    # get redirect target
    next_target = request.args.get('next')

    # make sure redirect target is safe
    if not is_safe_url(next_target):
        return abort(400)

    # redirect to next target or to user's boards page
    return redirect(next_target or url_for('user.boards', user_id=str(user.id)))

@auth.route('/logout', methods=['GET'])
def logout():
    """
    Logout route.
    """

    # logout the user
    logout_user()

    # render logout page
    return render_template('auth/logout.html')

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """
    Reset Password Request route.
    """

    # parse the form
    form = ResetPasswordRequestForm(request.form, obj=current_user)

    # render form if GET request
    if request.method == 'GET':
        return render_template('auth/reset-password-request.html', form=form)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('auth/reset-password-request.html', form=form), 400

    # send reset password email
    user = form.user
    token = TimedJSONWebSignatureSerializer(current_app.secret_key, expires_in=600) \
        .dumps(str(user.auth_id)) \
        .decode('utf-8')
    message = Message('Dawdle Password Reset', recipients=[user.email])
    message.html = render_template('auth/reset-password-email.html', user=user, token=token)
    try:
        mail.send(message)
        flash('A password reset email has been sent to {}. '.format(user.email) +
              'This will expire in 10 minutes.', 'success')
        return render_template('auth/reset-password-request.html', form=form)
    except:
        flash('Could not send a password reset email to {}. '.format(user.email) +
              'Please try again.', 'danger')
        return render_template('auth/reset-password-request.html', form=form), 500

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Reset Password route.
    """

    # make sure we have a valid token
    try:
        auth_id = TimedJSONWebSignatureSerializer(current_app.secret_key, expires_in=600).loads(token)
    except BadSignature:
        return abort(404)

    # make sure the user with the given auth id exists
    user = User.objects(auth_id=to_ObjectId(auth_id)).first()
    if user is None:
        abort(404)

    # parse the form
    form = ResetPasswordForm(request.form)

    # render form if GET request
    if request.method == 'GET':
        return render_template('auth/reset-password.html', form=form)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('auth/reset-password.html', form=form), 400

    # update the user's password (making sure to update the auth id and last updated)
    user.password = User.encrypt_password(form.password.data)
    user.auth_id = ObjectId()
    user.last_updated = datetime.utcnow()
    user.save()

    # notify the user
    flash('Your password has been reset.', 'success')

    # login the user
    login_user(user, remember=True)

    # redirect to user's boards page
    return redirect(url_for('user.boards', user_id=str(user.id)))
