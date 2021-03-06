from unittest.mock import patch

from bson.objectid import ObjectId

from dawdle.components.auth.utils import (_PASSWORD_RESET_TOKEN_EXPIRATION,
                                          _serialize_password_reset_token,
                                          _serialize_verification_token,
                                          activate_user, delete_user,
                                          encrypt_password,
                                          get_user_by_auth_id,
                                          get_user_by_email, get_user_by_id,
                                          get_user_from_password_reset_token,
                                          get_user_from_verification_token,
                                          save_new_user, send_deletion_email,
                                          send_password_reset_email,
                                          send_verification_email,
                                          update_user_email,
                                          update_user_password,
                                          verify_password)
from dawdle.extensions.sendgrid import TemplateIds
from tests.helpers import TestBase, fake


class TestUtils(TestBase):

    #
    # get_user_by_email tests.
    #

    def test_get_user_by_email_not_existing(self):
        assert not get_user_by_email(fake.email())

    def test_get_user_by_email(self):
        assert get_user_by_email(self._user.email) == self._user

    #
    # save_new_user tests.
    #

    def test_save_new_user(self):
        name = "john  peter smith richard david"
        email = fake.email()
        password = fake.password()
        user = save_new_user(name, email, password)
        assert user.initials == "JPSR"
        assert user.name == name.strip()
        assert verify_password(user.password, password)

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

    @patch("dawdle.components.auth.utils._serialize_verification_token")
    @patch("dawdle.components.auth.utils.sendgrid")
    def test_send_verification_email(self, sendgrid, serialize):
        token = fake.pystr()
        serialize.return_value = token
        send_verification_email(self._user)
        sendgrid.send.assert_called_with(
            TemplateIds.VERIFICATION,
            self._user.email,
            {
                "name": self._user.name,
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
        token = _serialize_verification_token(fake.sentence())
        assert not get_user_from_verification_token(token)

    def test_get_user_from_verification_token(self):
        token = _serialize_verification_token(self._user)
        assert self._user == get_user_from_verification_token(token)

    #
    # get_user_by_auth_id tests.
    #

    def test_get_user_by_auth_id_not_existing(self):
        assert not get_user_by_auth_id(ObjectId())

    def test_get_user_by_auth_id(self):
        assert get_user_by_auth_id(self._user.auth_id) == self._user

    #
    # activate_user tests.
    #

    def test_activate_user(self):
        user = self._create_user(active=False)
        old_user = get_user_by_email(user.email)
        user = activate_user(user)
        assert user.active
        assert user.auth_id != old_user.auth_id
        assert user.last_updated != old_user.last_updated
        assert user.updated_by == old_user

    #
    # send_password_reset_email tests.
    #

    @patch("dawdle.components.auth.utils._serialize_password_reset_token")
    @patch("dawdle.components.auth.utils.sendgrid")
    def test_send_password_reset_email(self, sendgrid, serialize):
        token = fake.pystr()
        serialize.return_value = token
        send_password_reset_email(self._user)
        sendgrid.send.assert_called_with(
            TemplateIds.PASSWORD_RESET,
            self._user.email,
            {
                "name": self._user.name,
                "token": token,
                "expiration": _PASSWORD_RESET_TOKEN_EXPIRATION,
            },
        )

    #
    # get_user_from_password_reset_token tests.
    #

    def test_get_user_from_password_reset_token_bad_token(self):
        token = fake.sentence()
        assert not get_user_from_password_reset_token(token)

    def test_get_user_from_password_reset_token_bad_auth_id(self):
        token = _serialize_password_reset_token(fake.sentence())
        assert not get_user_from_password_reset_token(token)

    def test_get_user_from_password_reset_token_expired(self):
        token = _serialize_password_reset_token(self._user, expires_in=-6000)
        assert not get_user_from_password_reset_token(token)

    def test_get_user_from_password_reset_token(self):
        token = _serialize_password_reset_token(self._user)
        assert self._user == get_user_from_password_reset_token(token)

    #
    # update_user_password tests.
    #

    def test_update_user_password(self):
        user = self._create_user()
        old_user = get_user_by_email(user.email)
        password = fake.password()
        user = update_user_password(user, password)
        assert user.auth_id != old_user.auth_id
        assert user.last_updated != old_user.last_updated
        assert verify_password(user.password, password)
        assert user.updated_by == old_user

    #
    # get_user_by_id tests.
    #

    def test_get_user_by_id_not_existing(self):
        assert not get_user_by_id(ObjectId())

    def test_get_user_by_id(self):
        assert get_user_by_id(self._user.id) == self._user

    #
    # delete_user tests.
    #

    def test_delete_user(self):
        user = self._create_user()
        user = delete_user(user)
        assert not get_user_by_id(user.id)

    #
    # send_password_reset_email tests.
    #

    @patch("dawdle.components.auth.utils.sendgrid")
    def test_send_deletion_email(self, sendgrid):
        send_deletion_email(self._user)
        sendgrid.send.assert_called_with(
            TemplateIds.ACCOUNT_DELETION,
            self._user.email,
            {"name": self._user.name},
        )

    #
    # update_user_email tests.
    #

    def test_update_user_email(self):
        user = self._create_user()
        old_user = get_user_by_email(user.email)
        email = fake.email()
        user = update_user_email(user, email)
        assert not user.active
        assert user.auth_id != old_user.auth_id
        assert user.email == email
        assert user.last_updated != old_user.last_updated
        assert user.updated_by == old_user
