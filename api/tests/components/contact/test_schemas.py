from dawdle.components.contact.schemas import contact_schema
from dawdle.extensions.marshmallow import Limits
from tests.components.contact.helpers import get_mock_contact_body
from tests.helpers import fake


class TestSchemas:

    def test_ContactSchema_no_email(self):
        body = get_mock_contact_body()
        del body["email"]
        errors = contact_schema.validate(body)
        assert errors == {
            "email": [
                "Missing data for required field.",
            ],
        }

    def test_ContactSchema_blank_email(self):
        body = get_mock_contact_body(email=" ")
        errors = contact_schema.validate(body)
        assert errors == {
            "email": [
                "Missing data for required field.",
            ],
        }

    def test_ContactSchema_invalid_email(self):
        email = fake.sentence()
        body = get_mock_contact_body(email=email)
        errors = contact_schema.validate(body)
        assert errors == {
            "email": [
                "Not a valid email address.",
            ],
        }

    def test_ContactSchema_trims_email(self):
        email = fake.email()
        body = get_mock_contact_body(email=f"  {email}  ")
        errors = contact_schema.validate(body)
        assert not errors
        dumped = contact_schema.dump(body)
        assert dumped["email"] == email

    def test_ContactSchema_no_subject(self):
        body = get_mock_contact_body()
        del body["subject"]
        errors = contact_schema.validate(body)
        assert errors == {
            "subject": [
                "Missing data for required field.",
            ],
        }

    def test_ContactSchema_blank_subject(self):
        body = get_mock_contact_body(subject=" ")
        errors = contact_schema.validate(body)
        assert errors == {
            "subject": [
                "Missing data for required field.",
            ],
        }

    def test_ContactSchema_subject_equal_to_max(self):
        subject = fake.pystr(
            min_chars=Limits.MAX_CONTACT_SUBJECT_LENGTH,
            max_chars=Limits.MAX_CONTACT_SUBJECT_LENGTH,
        )
        body = get_mock_contact_body(subject=subject)
        errors = contact_schema.validate(body)
        assert not errors

    def test_ContactSchema_subject_greater_than_max(self):
        subject = fake.pystr(
            min_chars=Limits.MAX_CONTACT_SUBJECT_LENGTH + 1,
            max_chars=Limits.MAX_CONTACT_SUBJECT_LENGTH + 1,
        )
        body = get_mock_contact_body(subject=subject)
        errors = contact_schema.validate(body)
        assert errors == {
            "subject": [
                "Longer than maximum length "
                f"{Limits.MAX_CONTACT_SUBJECT_LENGTH}.",
            ],
        }

    def test_ContactSchema_trims_subject(self):
        subject = fake.sentence()
        body = get_mock_contact_body(subject=f"  {subject}  ")
        errors = contact_schema.validate(body)
        assert not errors
        dumped = contact_schema.dump(body)
        assert dumped["subject"] == subject

    def test_ContactSchema_no_message(self):
        body = get_mock_contact_body()
        del body["message"]
        errors = contact_schema.validate(body)
        assert errors == {
            "message": [
                "Missing data for required field.",
            ],
        }

    def test_ContactSchema_blank_message(self):
        body = get_mock_contact_body(message=" ")
        errors = contact_schema.validate(body)
        assert errors == {
            "message": [
                "Missing data for required field.",
            ],
        }

    def test_ContactSchema_message_equal_to_max(self):
        message = fake.pystr(
            min_chars=Limits.MAX_CONTACT_MESSAGE_LENGTH,
            max_chars=Limits.MAX_CONTACT_MESSAGE_LENGTH,
        )
        body = get_mock_contact_body(message=message)
        errors = contact_schema.validate(body)
        assert not errors

    def test_ContactSchema_message_greater_than_max(self):
        message = fake.pystr(
            min_chars=Limits.MAX_CONTACT_MESSAGE_LENGTH + 1,
            max_chars=Limits.MAX_CONTACT_MESSAGE_LENGTH + 1,
        )
        body = get_mock_contact_body(message=message)
        errors = contact_schema.validate(body)
        assert errors == {
            "message": [
                "Longer than maximum length "
                f"{Limits.MAX_CONTACT_MESSAGE_LENGTH}.",
            ],
        }

    def test_ContactSchema_trims_message(self):
        message = fake.sentence()
        body = get_mock_contact_body(message=f"  {message}  ")
        errors = contact_schema.validate(body)
        assert not errors
        dumped = contact_schema.dump(body)
        assert dumped["message"] == message
