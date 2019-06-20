from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user
from flask_mail import Message

from dawdle.extensions.mail import mail
from dawdle.forms.contact import ContactForm

contact = Blueprint('contact', __name__, url_prefix='/contact')

@contact.route('/')
def index_GET():
    return render_template('contact/index.html', form=ContactForm(request.form, obj=current_user))

@contact.route('/', methods=['POST'])
def index_POST():
    form = ContactForm(request.form, obj=current_user)

    if not form.validate_on_submit():
        return render_template('contact/index.html', form=form), 400

    sent_email = _send_email(form)

    if not sent_email:
        flash('Could not send message. Please try again.', 'danger')
        return render_template('contact/index.html', form=form), 500

    flash('We have received your message. Somebody will get back to you shortly.', 'success')
    return redirect(url_for('contact.index_GET'))

def _send_email(form):
    try:
        message = Message('Dawdle: {}'.format(form.subject.data), recipients=[current_app.config['CONTACT_EMAIL']])
        message.body = 'From: {}\n\n{}'.format(form.email.data, form.message.data)
        mail.send(message)
        return True
    except:
        return False
