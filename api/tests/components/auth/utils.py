from tests.utils import fake


def get_mock_sign_up_body(**kwargs):
    return {
        "email": kwargs.get("email", fake.email()),
        "name": kwargs.get("name", fake.name()),
        "password": kwargs.get("password", fake.password()),
    }
