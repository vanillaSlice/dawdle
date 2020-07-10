from flask import current_app

from dawdle.extensions.sendgrid import TemplateIds, sendgrid


def send_contact_emails(email, subject, message):
    data = {
        "email": email,
        "subject": subject,
        "message": message,
    }

    sendgrid.send(
        TemplateIds.CONTACT_RECEIVER,
        current_app.config["CONTACT_EMAIL"],
        data,
    )

    sendgrid.send(TemplateIds.CONTACT_SENDER, email, data)
