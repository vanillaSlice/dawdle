from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from dawdle.forms.contact import ContactForm
from dawdle.utils import send_contact_emails

contact_bp = Blueprint('contact', __name__, url_prefix='/contact')


@contact_bp.route('/')
def index_GET():
    form = ContactForm(request.form, obj=current_user)
    return render_template('contact/index.html', form=form)


@contact_bp.route('/', methods=['POST'])
def index_POST():
    form = ContactForm(request.form, obj=current_user)

    if not form.validate_on_submit():
        return render_template('contact/index.html', form=form), 400

    sent_email = send_contact_emails(
        subject=form.subject.data,
        email=form.email.data,
        message=form.message.data,
    )

    if not sent_email:
        return render_template('contact/index.html', form=form), 500

    return redirect(url_for('contact.index_GET'))
