from datetime import datetime

from bson.objectid import ObjectId
from flask import abort, Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from flask_mail import Message
from itsdangerous import BadSignature, TimedJSONWebSignatureSerializer, URLSafeSerializer

from dawdle.extensions.mail import mail
from dawdle.forms.auth import LoginForm, ResetPasswordForm, ResetPasswordRequestForm, SignUpForm, VerifyResendForm
from dawdle.models.user import User
from dawdle.utils import is_safe_url, send_verification_email, to_ObjectId

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/sign-up')
def sign_up_GET():
    return render_template('auth/sign-up.html', form=SignUpForm(request.form))

@auth.route('/sign-up', methods=['POST'])
def sign_up_POST():
    form = SignUpForm(request.form)

    if not form.validate_on_submit():
        return render_template('auth/sign-up.html', form=form), 400

    user = User()
    form.populate_obj(user)
    user.initials = ''.join([s[0].upper() for s in user.name.split(' ')])[:4]
    user.password = User.encrypt_password(form.password.data)
    user.save()

    send_verification_email(user)

    return redirect(url_for('auth.verify_resend_GET', email=form.email.data))

@auth.route('/verify/resend')
def verify_resend_GET():
    form = VerifyResendForm(request.form, email=request.args.get('email'))
    return render_template('auth/verify-resend.html', form=form)

@auth.route('/verify/resend', methods=['POST'])
def verify_resend_POST():
    form = VerifyResendForm(request.form, email=request.args.get('email'))

    if not form.validate_on_submit():
        return render_template('auth/verify-resend.html', form=form), 400

    sent_email = send_verification_email(form.user, request.args.get('next'))
    status_code = 200 if sent_email else 500

    return render_template('auth/verify-resend.html', form=form), status_code

@auth.route('/verify/<token>')
def verify_GET(token):
    try:
        auth_id = URLSafeSerializer(current_app.secret_key).loads(token)
    except BadSignature:
        abort(404)

    user = User.objects(auth_id=to_ObjectId(auth_id)).first()
    if user is None:
        abort(404)

    user.active = True
    user.auth_id = ObjectId()
    user.last_updated = datetime.utcnow()
    user.save()

    login_user(user)

    flash('Your email address has been verified.', 'success')

    next_target = request.args.get('next')

    if not is_safe_url(next_target):
        abort(400)

    return redirect(next_target or url_for('user.boards_GET'))

@auth.route('/login')
def login_GET():
    return render_template('auth/login.html', form=LoginForm(request.form))

@auth.route('/login', methods=['POST'])
def login_POST():
    form = LoginForm(request.form)

    if not form.validate_on_submit():
        return render_template('auth/login.html', form=form), 400

    login_user(form.user, remember=form.remember_me.data)

    next_target = request.args.get('next')

    if not is_safe_url(next_target):
        abort(400)

    return redirect(next_target or url_for('user.boards_GET'))

@auth.route('/logout')
def logout_GET():
    logout_user()

    flash('You have been logged out.', 'info')

    return redirect(url_for('home.index_GET'))

@auth.route('/reset-password')
def reset_password_request_GET():
    form = ResetPasswordRequestForm(request.form, obj=current_user)
    return render_template('auth/reset-password-request.html', form=form)

@auth.route('/reset-password', methods=['POST'])
def reset_password_request_POST():
    form = ResetPasswordRequestForm(request.form, obj=current_user)

    if not form.validate_on_submit():
        return render_template('auth/reset-password-request.html', form=form), 400

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
    _verify_reset_password_token(token)
    return render_template('auth/reset-password.html', form=ResetPasswordForm(request.form))

@auth.route('/reset-password/<token>', methods=['POST'])
def reset_password_POST(token):
    user = _verify_reset_password_token(token)

    form = ResetPasswordForm(request.form)

    if not form.validate_on_submit():
        return render_template('auth/reset-password.html', form=form), 400

    user.password = User.encrypt_password(form.password.data)
    user.auth_id = ObjectId()
    user.last_updated = datetime.utcnow()
    user.save()

    flash('Your password has been reset.', 'success')

    login_user(user)

    return redirect(url_for('user.boards_GET'))

def _verify_reset_password_token(token):
    try:
        auth_id = TimedJSONWebSignatureSerializer(current_app.secret_key, expires_in=600).loads(token)
    except BadSignature:
        abort(404)

    user = User.objects(auth_id=to_ObjectId(auth_id)).first()
    if user is None:
        abort(404)

    return user
