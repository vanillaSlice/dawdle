from dawdle.components.auth.schemas import (email_password_schema,
                                            email_schema, password_schema,
                                            sign_up_schema)
from dawdle.utils.schemas import Limits
from tests.components.auth.helpers import (get_mock_email_body,
                                           get_mock_email_password_body,
                                           get_mock_password_body,
                                           get_mock_sign_up_body)
from tests.helpers import fake


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

    def test_SignUpSchema_name_equal_to_max(self):
        name = fake.pystr(
            min_chars=Limits.MAX_USER_NAME_LENGTH,
            max_chars=Limits.MAX_USER_NAME_LENGTH,
        )
        body = get_mock_sign_up_body(name=name)
        errors = sign_up_schema.validate(body)
        assert not errors

    def test_SignUpSchema_name_greater_than_max(self):
        name = fake.pystr(
            min_chars=Limits.MAX_USER_NAME_LENGTH + 1,
            max_chars=Limits.MAX_USER_NAME_LENGTH + 1,
        )
        body = get_mock_sign_up_body(name=name)
        errors = sign_up_schema.validate(body)
        assert errors == {
            "name": [
                f"Longer than maximum length {Limits.MAX_USER_NAME_LENGTH}.",
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
        password = fake.pystr(
            min_chars=Limits.MIN_USER_PASSWORD_LENGTH - 1,
            max_chars=Limits.MIN_USER_PASSWORD_LENGTH - 1,
        )
        body = get_mock_sign_up_body(password=password)
        errors = sign_up_schema.validate(body)
        assert errors == {
            "password": [
                f"Length must be between {Limits.MIN_USER_PASSWORD_LENGTH} "
                f"and {Limits.MAX_USER_PASSWORD_LENGTH}.",
            ],
        }

    def test_SignUpSchema_password_equal_to_min(self):
        password = fake.pystr(
            min_chars=Limits.MIN_USER_PASSWORD_LENGTH,
            max_chars=Limits.MIN_USER_PASSWORD_LENGTH,
        )
        body = get_mock_sign_up_body(password=password)
        errors = sign_up_schema.validate(body)
        assert not errors

    def test_SignUpSchema_password_equal_to_max(self):
        password = fake.pystr(
            min_chars=Limits.MAX_USER_PASSWORD_LENGTH,
            max_chars=Limits.MAX_USER_PASSWORD_LENGTH,
        )
        body = get_mock_sign_up_body(password=password)
        errors = sign_up_schema.validate(body)
        assert not errors

    def test_SignUpSchema_password_greater_than_max(self):
        password = fake.pystr(
            min_chars=Limits.MAX_USER_PASSWORD_LENGTH + 1,
            max_chars=Limits.MAX_USER_PASSWORD_LENGTH + 1,
        )
        body = get_mock_sign_up_body(password=password)
        errors = sign_up_schema.validate(body)
        assert errors == {
            "password": [
                f"Length must be between {Limits.MIN_USER_PASSWORD_LENGTH} "
                f"and {Limits.MAX_USER_PASSWORD_LENGTH}.",
            ],
        }

    def test_SignUpSchema_unrecognised_field(self):
        body = get_mock_sign_up_body()
        key = fake.pystr()
        body[key] = fake.pystr()
        assert not sign_up_schema.validate(body)
        assert key not in sign_up_schema.dump(body)

    #
    # EmailSchema tests.
    #

    def test_EmailSchema_no_email(self):
        body = get_mock_email_body()
        del body["email"]
        errors = email_schema.validate(body)
        assert errors == {
            "email": [
                "Missing data for required field.",
            ],
        }

    def test_EmailSchema_invalid_email(self):
        email = fake.sentence()
        body = get_mock_email_body(email=email)
        errors = email_schema.validate(body)
        assert errors == {
            "email": [
                "Not a valid email address.",
            ],
        }

    def test_EmailSchema_unrecognised_field(self):
        body = get_mock_email_body()
        key = fake.pystr()
        body[key] = fake.pystr()
        assert not email_schema.validate(body)
        assert key not in email_schema.dump(body)

    #
    # EmailPasswordSchema tests.
    #

    def test_EmailPasswordSchema_no_email(self):
        body = get_mock_email_password_body()
        del body["email"]
        errors = email_password_schema.validate(body)
        assert errors == {
            "email": [
                "Missing data for required field.",
            ],
        }

    def test_EmailPasswordSchema_invalid_email(self):
        email = fake.sentence()
        body = get_mock_email_password_body(email=email)
        errors = email_password_schema.validate(body)
        assert errors == {
            "email": [
                "Not a valid email address.",
            ],
        }

    def test_EmailPasswordSchema_no_password(self):
        body = get_mock_email_password_body()
        del body["password"]
        errors = email_password_schema.validate(body)
        assert errors == {
            "password": [
                "Missing data for required field.",
            ],
        }

    def test_EmailPasswordSchema_unrecognised_field(self):
        body = get_mock_email_password_body()
        key = fake.pystr()
        body[key] = fake.pystr()
        assert not email_password_schema.validate(body)
        assert key not in email_password_schema.dump(body)

    #
    # PasswordSchema tests.
    #

    def test_PasswordSchema_no_password(self):
        body = get_mock_password_body()
        del body["password"]
        errors = password_schema.validate(body)
        assert errors == {
            "password": [
                "Missing data for required field.",
            ],
        }

    def test_PasswordSchema_password_less_than_min(self):
        password = fake.pystr(
            min_chars=Limits.MIN_USER_PASSWORD_LENGTH - 1,
            max_chars=Limits.MIN_USER_PASSWORD_LENGTH - 1,
        )
        body = get_mock_password_body(password=password)
        errors = password_schema.validate(body)
        assert errors == {
            "password": [
                f"Length must be between {Limits.MIN_USER_PASSWORD_LENGTH} "
                f"and {Limits.MAX_USER_PASSWORD_LENGTH}.",
            ],
        }

    def test_PasswordSchema_password_equal_to_min(self):
        password = fake.pystr(
            min_chars=Limits.MIN_USER_PASSWORD_LENGTH,
            max_chars=Limits.MIN_USER_PASSWORD_LENGTH,
        )
        body = get_mock_password_body(password=password)
        errors = password_schema.validate(body)
        assert not errors

    def test_PasswordSchema_password_equal_to_max(self):
        password = fake.pystr(
            min_chars=Limits.MAX_USER_PASSWORD_LENGTH,
            max_chars=Limits.MAX_USER_PASSWORD_LENGTH,
        )
        body = get_mock_password_body(password=password)
        errors = password_schema.validate(body)
        assert not errors

    def test_PasswordSchema_password_greater_than_max(self):
        password = fake.pystr(
            min_chars=Limits.MAX_USER_PASSWORD_LENGTH + 1,
            max_chars=Limits.MAX_USER_PASSWORD_LENGTH + 1,
        )
        body = get_mock_password_body(password=password)
        errors = password_schema.validate(body)
        assert errors == {
            "password": [
                f"Length must be between {Limits.MIN_USER_PASSWORD_LENGTH} "
                f"and {Limits.MAX_USER_PASSWORD_LENGTH}.",
            ],
        }

    def test_PasswordSchema_unrecognised_field(self):
        body = get_mock_password_body()
        key = fake.pystr()
        body[key] = fake.pystr()
        assert not password_schema.validate(body)
        assert key not in password_schema.dump(body)
