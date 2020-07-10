from dawdle.components.contact.utils import send_contact_emails
from tests.helpers import TestBase, fake


class TestUtils(TestBase):

    def test_send_contact_emails(self):
        email = fake.email()
        subject = fake.sentence()
        message = fake.sentence()
        send_contact_emails(email, subject, message)
