from unittest.mock import patch

from dawdle.components.auth.utils import (create_initials, encrypt_password,
                                          get_user_from_password_reset_token,
                                          get_user_from_verification_token,
                                          send_password_reset_email,
                                          send_verification_email,
                                          serialize_password_reset_token,
                                          serialize_verification_token,
                                          verify_password)
from dawdle.extensions.sendgrid import TemplateIds
from tests.helpers import TestBase, fake


class TestUtils(TestBase):

    #
    # create_initials tests.
    #

    def test_create_initials(self):
        assert create_initials(" john  peter smith richard  david ") == "JPSR"

    #
    # encrypt_password / verify_password tests.
    #

    def test_encrypt_password_verify_password(self):
        password = fake.password()
        encrypted_password = encrypt_password(password)
        assert password != encrypted_password
        assert verify_password(encrypted_password, password)

    def test_encrypt_password_verify_password_incorrect(self):
        password = fake.password()
        encrypted_password = encrypt_password(password)
        assert password != encrypted_password
        assert not verify_password(encrypted_password, "wrong")

    def test_verify_password_None(self):
        password = fake.password()
        encrypted_password = encrypt_password(password)
        assert password != encrypted_password
        assert not verify_password(encrypted_password, None)

    #
    # send_verification_email tests.
    #

    @patch("dawdle.components.auth.utils.serialize_verification_token")
    @patch("dawdle.components.auth.utils.sendgrid")
    def test_send_verification_email(self, sendgrid, serialize):
        token = fake.pystr()
        serialize.return_value = token
        send_verification_email(self.user)
        sendgrid.send.assert_called_with(
            TemplateIds.VERIFICATION,
            self.user.email,
            data={
                "name": self.user.name,
                "token": token,
            },
        )

    #
    # get_user_from_verification_token tests.
    #

    def test_get_user_from_verification_token_bad_token(self):
        token = fake.sentence()
        assert not get_user_from_verification_token(token)

    def test_get_user_from_verification_token_bad_auth_id(self):
        token = serialize_verification_token(fake.sentence())
        assert not get_user_from_verification_token(token)

    def test_get_user_from_verification_token(self):
        token = serialize_verification_token(self.user)
        assert self.user == get_user_from_verification_token(token)

    #
    # send_password_reset_email tests.
    #

    @patch("dawdle.components.auth.utils.serialize_password_reset_token")
    @patch("dawdle.components.auth.utils.sendgrid")
    def test_send_password_reset_email(self, sendgrid, serialize):
        token = fake.pystr()
        serialize.return_value = token
        send_password_reset_email(self.user)
        sendgrid.send.assert_called_with(
            TemplateIds.PASSWORD_RESET,
            self.user.email,
            data={
                "name": self.user.name,
                "token": token,
                "expiration": 900,
            },
        )

    #
    # get_user_from_password_reset_token tests.
    #

    def test_get_user_from_password_reset_token_bad_token(self):
        token = fake.sentence()
        assert not get_user_from_password_reset_token(token)

    def test_get_user_from_password_reset_token_bad_auth_id(self):
        token = serialize_password_reset_token(fake.sentence())
        assert not get_user_from_password_reset_token(token)

    def test_get_user_from_password_reset_token(self):
        token = serialize_password_reset_token(self.user)
        assert self.user == get_user_from_password_reset_token(token)
