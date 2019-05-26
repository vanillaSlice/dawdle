"""
Exports Auth routes.
"""

from flask import abort, Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from flask_mail import Message
from itsdangerous import BadSignature, URLSafeSerializer

from dawdle.extensions import mail
from dawdle.forms.auth import LoginForm, SignUpForm, VerifyResendForm
from dawdle.models.user import User
from dawdle.utils import is_safe_url, to_ObjectId

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
    mail.send(message)
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
    Verify route.
    """

    # make sure we have a valid token
    try:
        user_id = URLSafeSerializer(current_app.secret_key).loads(token)
    except BadSignature:
        return abort(404)

    # make sure the user with the given id exists
    user = User.objects(id=to_ObjectId(user_id)).first()
    if user is None:
        abort(404)

    # user is already active so redirect to user's boards page
    if user.is_active:
        return redirect(url_for('user.boards', user_id=str(user.id)))

    # activate the user
    user.active = True
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
