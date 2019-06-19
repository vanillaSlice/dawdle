from urllib.parse import urljoin, urlparse

from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import current_app, flash, render_template, request
from flask_mail import Message
from itsdangerous import URLSafeSerializer

from dawdle.extensions.mail import mail

def to_ObjectId(value):
    try:
        return ObjectId(value)
    except InvalidId:
        return ObjectId(None)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def trim(s):
    return ' '.join(s.split())

def send_verification_email(user, redirect_target=None):
    token = URLSafeSerializer(current_app.secret_key).dumps(str(user.auth_id))
    message = Message('Dawdle Verification', recipients=[user.email])
    message.html = render_template('auth/verify-email.html', user=user, token=token, redirect_target=redirect_target)
    try:
        mail.send(message)
        flash('A verification email has been sent to {}. '.format(user.email) +
              'Please verify your email before logging in to Dawdle.', 'info')
        return True
    except:
        flash('Could not send a verification email to {}. '.format(user.email) +
              'Please try again.', 'danger')
        return False
