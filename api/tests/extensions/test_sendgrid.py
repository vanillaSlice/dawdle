from unittest.mock import patch

from dawdle.extensions.sendgrid import sendgrid


class MockApp:

    config = {
        "SENDGRID_API_KEY": "some-api-key",
        "SENDER_EMAIL": "some-email",
    }


class TestSendGrid:

    @patch("dawdle.extensions.sendgrid.SendGridAPIClient")
    def test_send(self, client):
        app = MockApp()

        sendgrid.init_app(app)

        template_id = "some-template-id"
        recipient = "some-recipient"
        data = {
            "some": "data",
            "more": "data",
        }

        sendgrid.send(template_id, recipient, data)

        message = client().send.call_args[0][0]

        assert message.from_email.name == "Dawdle"
        assert message.from_email.email == app.config["SENDER_EMAIL"]
        assert message.personalizations[0].tos[0]["name"] == recipient
        assert message.template_id.template_id == template_id
        assert message.personalizations[0].dynamic_template_data == data
