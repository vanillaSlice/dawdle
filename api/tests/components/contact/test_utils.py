from unittest.mock import call, patch

from dawdle.components.contact.utils import send_contact_emails
from dawdle.extensions.sendgrid import TemplateIds
from tests.helpers import TestBase, fake


class TestUtils(TestBase):

    @patch("dawdle.components.contact.utils.sendgrid")
    def test_send_contact_emails(self, sengrid):
        receiver = fake.email()
        self._app.config.update({"CONTACT_EMAIL": receiver})
        sender = fake.email()
        subject = fake.sentence()
        message = fake.sentence()
        send_contact_emails(sender, subject, message)
        data = {
            "email": sender,
            "subject": subject,
            "message": message,
        }
        sengrid.send.assert_has_calls([
            call(TemplateIds.CONTACT_RECEIVER, receiver, data),
            call(TemplateIds.CONTACT_SENDER, sender, data),
        ], any_order=True)
