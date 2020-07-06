# pylint: disable=no-self-use

from dawdle.components.auth.schemas import sign_up_schema
from tests.components.auth.utils import get_mock_sign_up_body
from tests.utils import fake


class TestSchemas:

    #
    # SignUpSchema tests.
    #

    def test_SignUpSchema_no_name(self):
        body = get_mock_sign_up_body()
        del body["name"]
        errors = sign_up_schema.validate(body)
        assert errors == {
            "name": [
                "Missing data for required field.",
            ],
        }

    def test_SignUpSchema_blank_name(self):
        body = get_mock_sign_up_body(name=" ")
        errors = sign_up_schema.validate(body)
        assert errors == {
            "name": [
                "Missing data for required field.",
            ],
        }

    def test_SignUpSchema_name_equal_to_min(self):
        name = fake.pystr(min_chars=1, max_chars=1)
        body = get_mock_sign_up_body(name=name)
        errors = sign_up_schema.validate(body)
        assert not errors

    def test_SignUpSchema_name_equal_to_max(self):
        name = fake.pystr(min_chars=50, max_chars=50)
        body = get_mock_sign_up_body(name=name)
        errors = sign_up_schema.validate(body)
        assert not errors

    def test_SignUpSchema_name_greater_than_max(self):
        name = fake.pystr(min_chars=51, max_chars=51)
        body = get_mock_sign_up_body(name=name)
        errors = sign_up_schema.validate(body)
        assert errors == {
            "name": [
                "Length must be between 1 and 50.",
            ],
        }

    def test_SignUpSchema_trims_name(self):
        body = get_mock_sign_up_body(name="  John  Smith  ")
        errors = sign_up_schema.validate(body)
        assert not errors
        dumped = sign_up_schema.dump(body)
        assert dumped["name"] == "John Smith"

    def test_SignUpSchema_no_email(self):
        body = get_mock_sign_up_body()
        del body["email"]
        errors = sign_up_schema.validate(body)
        assert errors == {
            "email": [
                "Missing data for required field.",
            ],
        }

    def test_SignUpSchema_invalid_email(self):
        email = fake.sentence()
        body = get_mock_sign_up_body(email=email)
        errors = sign_up_schema.validate(body)
        assert errors == {
            "email": [
                "Not a valid email address.",
            ],
        }

    def test_SignUpSchema_no_password(self):
        body = get_mock_sign_up_body()
        del body["password"]
        errors = sign_up_schema.validate(body)
        assert errors == {
            "password": [
                "Missing data for required field.",
            ],
        }

    def test_SignUpSchema_password_less_than_min(self):
        password = fake.pystr(min_chars=7, max_chars=7)
        body = get_mock_sign_up_body(password=password)
        errors = sign_up_schema.validate(body)
        assert errors == {
            "password": [
                "Shorter than minimum length 8.",
            ],
        }

    def test_SignUpSchema_password_equal_to_min(self):
        password = fake.pystr(min_chars=8, max_chars=8)
        body = get_mock_sign_up_body(password=password)
        errors = sign_up_schema.validate(body)
        assert not errors
