from unittest.mock import patch

from dawdle.extensions.sendgrid import sendgrid
from tests.utils import fake


class MockApp:

    config = {
        "SENDGRID_API_KEY": fake.pystr(),
        "SENDER_EMAIL": fake.email(),
    }


class TestSendGrid:

    @patch("dawdle.extensions.sendgrid.SendGridAPIClient")
    def test_send(self, client):
        app = MockApp()

        sendgrid.init_app(app)

        template_id = fake.pystr()
        recipient = fake.email()
        data = fake.pydict(4, True, "str")

        sendgrid.send(template_id, recipient, data)

        message = client().send.call_args[0][0]

        assert message.from_email.name == "Dawdle"
        assert message.from_email.email == app.config["SENDER_EMAIL"]
        assert message.personalizations[0].tos[0]["email"] == recipient
        assert message.template_id.template_id == template_id
        assert message.personalizations[0].dynamic_template_data == data
