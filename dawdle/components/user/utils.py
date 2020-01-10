from flask import render_template
from flask_mail import Message

from dawdle.extensions.mail import mail


def send_delete_account_email(user):
    try:
        recipients = [user.email]
        msg = Message('Account Deleted', recipients=recipients)
        msg.html = render_template(
            'user/settings-delete-account-email.html',
            user=user,
        )
        mail.send(msg)
        return True
    except Exception:
        return False
