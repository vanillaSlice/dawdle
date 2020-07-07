from tests.helpers import fake


def get_mock_sign_up_body(**kwargs):
    return {
        "email": kwargs.get("email", fake.email()),
        "name": kwargs.get("name", fake.name()),
        "password": kwargs.get("password", fake.password()),
    }


def get_mock_email_body(**kwargs):
    return {
        "email": kwargs.get("email", fake.email()),
    }


def get_mock_email_password_body(**kwargs):
    return {
        "email": kwargs.get("email", fake.email()),
        "password": kwargs.get("password", fake.password()),
    }


def get_mock_password_body(**kwargs):
    return {
        "password": kwargs.get("password", fake.password()),
    }
