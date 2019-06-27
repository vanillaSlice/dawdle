from urllib.parse import urljoin, urlparse

from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import current_app, flash, render_template, request
from flask_mail import Message
from itsdangerous import (BadSignature,
                          TimedJSONWebSignatureSerializer,
                          URLSafeSerializer)

from dawdle.extensions.mail import mail


def to_ObjectId(value):
    try:
        return ObjectId(value)
    except InvalidId:
        return ObjectId(None)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def normalize_whitespace(s):
    return ' '.join(s.split())


def remove_whitespace(s):
    return ''.join(s.split())


def strip(s):
    return s.strip()


def upper(s):
    return s.upper()


def serialize_verification_token(user):
    return URLSafeSerializer(current_app.secret_key).dumps(str(user.auth_id))


def deserialize_verification_token(token):
    try:
        auth_id = URLSafeSerializer(current_app.secret_key).loads(token)
        return to_ObjectId(auth_id)
    except BadSignature:
        return to_ObjectId(None)


def send_verification_email(user, redirect_target=None):
    try:
        recipients = [user.email]
        msg = Message('Dawdle Verification', recipients=recipients)
        msg.html = render_template(
            'auth/verify-email.html',
            user=user,
            token=serialize_verification_token(user),
            redirect_target=redirect_target,
        )
        mail.send(msg)
        flash(
            'A verification email has been sent to {}. Please verify your '
            'email before logging in to Dawdle.'.format(user.email),
            'info',
        )
        return True
    except Exception:
        flash(
            'Could not send a verification email to {}. Please try again.'
            .format(user.email),
            'danger',
        )
        return False


def serialize_password_reset_token(user):
    return TimedJSONWebSignatureSerializer(
        current_app.secret_key,
        expires_in=600,
    ).dumps(str(user.auth_id)).decode('utf-8')


def deserialize_password_reset_token(token):
    try:
        auth_id = TimedJSONWebSignatureSerializer(
            current_app.secret_key,
            expires_in=600,
        ).loads(token)
        return to_ObjectId(auth_id)
    except BadSignature:
        return to_ObjectId(None)


def send_password_reset_email(user):
    try:
        recipients = [user.email]
        msg = Message('Dawdle Password Reset', recipients=[user.email])
        msg.html = render_template(
            'auth/reset-password-email.html',
            user=user,
            token=serialize_password_reset_token(user),
        )
        mail.send(msg)
        flash(
            'A password reset email has been sent to {}. This will expire in '
            '10 minutes.'.format(user.email),
            'info',
        )
        return True
    except Exception:
        flash(
            'Could not send a password reset email to {}. Please try again.'
            .format(user.email),
            'danger',
        )
        return False


def send_delete_account_email(user):
    try:
        recipients = [user.email]
        msg = Message('Dawdle Account Deleted', recipients=recipients)
        msg.html = render_template(
            'user/settings-delete-account-email.html',
            user=user,
        )
        mail.send(msg)
        return True
    except Exception:
        return False


def send_contact_emails(subject, email, message):
    try:
        recipients = [current_app.config['MAIL_USERNAME']]
        msg = Message('Dawdle: {}'.format(subject), recipients=recipients)
        msg.body = 'From: {}\n\n{}'.format(email, message)
        mail.send(msg)
        recipients = [email]
        msg = Message('Dawdle: {}'.format(subject), recipients=recipients)
        msg.html = render_template('contact/email.html', message=message)
        mail.send(msg)
        flash(
            'We have received your message. '
            'Somebody will get back to you shortly.',
            'success',
        )
        return True
    except Exception:
        flash('Could not send message. Please try again.', 'danger')
        return False
