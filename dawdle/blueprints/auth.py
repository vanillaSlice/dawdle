"""
Exports Auth blueprint.
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
              'Please verify your email before logging in to Dawdle.', 'info')
        return True
    except:
        flash('Could not send a verification email to {}. '.format(user.email) +
              'Please try again.', 'danger')
        return False

def verify_reset_password_token(token):
    """
    Verifies reset password token, returning the user if successful.
    """

    # make sure we have a valid token
    try:
        auth_id = TimedJSONWebSignatureSerializer(current_app.secret_key, expires_in=600).loads(token)
    except BadSignature:
        abort(404)

    # make sure the user with the given auth id exists
    user = User.objects(auth_id=to_ObjectId(auth_id)).first()
    if user is None:
        abort(404)

    return user

#
# Routes
#

@auth.route('/sign-up')
def sign_up_GET():
    """
    Sign Up GET route.
    """

    return render_template('auth/sign-up.html', form=SignUpForm(request.form))

@auth.route('/sign-up', methods=['POST'])
def sign_up_POST():
    """
    Sign Up POST route.
    """

    # parse the form
    form = SignUpForm(request.form)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('auth/sign-up.html', form=form), 400

    # save new user
    user = User()
    form.populate_obj(user)
    user.initials = ''.join([s[0].upper() for s in user.name.split(' ')])[:4]
    user.password = User.encrypt_password(form.password.data)
    user.save()

    # send verification email
    send_verification_email(user)

    # redirect to verify resend page
    return redirect(url_for('auth.verify_resend_GET', email=form.email.data))

@auth.route('/verify/resend')
def verify_resend_GET():
    """
    Verify Resend GET route.
    """

    form = VerifyResendForm(request.form, email=request.args.get('email'))
    return render_template('auth/verify-resend.html', form=form)

@auth.route('/verify/resend', methods=['POST'])
def verify_resend_POST():
    """
    Verify Resend POST route.
    """

    # parse the form
    form = VerifyResendForm(request.form, email=request.args.get('email'))

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('auth/verify-resend.html', form=form), 400

    # send verification email
    sent_email = send_verification_email(form.user)
    status_code = 200 if sent_email else 500

    # render form again
    return render_template('auth/verify-resend.html', form=form), status_code

@auth.route('/verify/<token>')
def verify_GET(token):
    """
    Verify GET route.
    """

    # make sure we have a valid token
    try:
        auth_id = URLSafeSerializer(current_app.secret_key).loads(token)
    except BadSignature:
        abort(404)

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
    login_user(user)

    # notify the user
    flash('Your user registration was successful.', 'success')

    # redirect to user's boards page
    return redirect(url_for('user.boards_GET'))

@auth.route('/login')
def login_GET():
    """
    Login GET route.
    """

    return render_template('auth/login.html', form=LoginForm(request.form))

@auth.route('/login', methods=['POST'])
def login_POST():
    """
    Login POST route.
    """

    # parse the form
    form = LoginForm(request.form)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('auth/login.html', form=form), 400

    # login the user
    login_user(form.user, remember=form.remember_me.data)

    # get redirect target
    next_target = request.args.get('next')

    # make sure redirect target is safe
    if not is_safe_url(next_target):
        abort(400)

    # redirect to next target or to user's boards page
    return redirect(next_target or url_for('user.boards_GET'))

@auth.route('/logout')
def logout_GET():
    """
    Logout GET route.
    """

    # logout the user
    logout_user()

    # notify the user
    flash('You have been logged out.', 'info')

    # render home page
    return redirect(url_for('home.index_GET'))

@auth.route('/reset-password')
def reset_password_request_GET():
    """
    Reset Password Request GET route.
    """

    form = ResetPasswordRequestForm(request.form, obj=current_user)
    return render_template('auth/reset-password-request.html', form=form)

@auth.route('/reset-password', methods=['POST'])
def reset_password_request_POST():
    """
    Reset Password Request POST route.
    """

    # parse the form
    form = ResetPasswordRequestForm(request.form, obj=current_user)

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
              'This will expire in 10 minutes.', 'info')
        return render_template('auth/reset-password-request.html', form=form)
    except:
        flash('Could not send a password reset email to {}. '.format(user.email) +
              'Please try again.', 'danger')
        return render_template('auth/reset-password-request.html', form=form), 500

@auth.route('/reset-password/<token>')
def reset_password_GET(token):
    """
    Reset Password GET route.
    """

    verify_reset_password_token(token)

    return render_template('auth/reset-password.html', form=ResetPasswordForm(request.form))

@auth.route('/reset-password/<token>', methods=['POST'])
def reset_password_POST(token):
    """
    Reset Password POST route.
    """

    user = verify_reset_password_token(token)

    # parse the form
    form = ResetPasswordForm(request.form)

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
    login_user(user)

    # redirect to user's boards page
    return redirect(url_for('user.boards_GET'))
