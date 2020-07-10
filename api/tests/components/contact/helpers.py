from tests.helpers import fake


def get_mock_contact_body(**kwargs):
    return {
        "email": kwargs.get("email", fake.email()),
        "subject": kwargs.get("subject", fake.sentence()),
        "message": kwargs.get("message", fake.sentence()),
    }
