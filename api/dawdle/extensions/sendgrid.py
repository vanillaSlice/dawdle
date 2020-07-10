from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendGrid:

    def __init__(self):
        self.__app = None
        self.__client = None

    def init_app(self, app):
        self.__app = app
        self.__client = SendGridAPIClient(
            self.__app.config["SENDGRID_API_KEY"],
        )

    def send(self, template_id, recipient, data):
        message = Mail(
            from_email=(self.__app.config["SENDER_EMAIL"], "Dawdle"),
            to_emails=recipient,
        )

        message.template_id = template_id

        message.dynamic_template_data = data

        self.__client.send(message)


sendgrid = SendGrid()


class TemplateIds:

    DELETION = "d-412a7cabd3cf48379be544be8dcd7823"  # update this
    PASSWORD_RESET = "d-de72675553af4e1ba8ff10237ed680ab"
    VERIFICATION = "d-412a7cabd3cf48379be544be8dcd7823"
