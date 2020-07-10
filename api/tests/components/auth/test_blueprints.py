import json
from unittest.mock import patch

from flask import url_for

from dawdle.components.auth.utils import (_serialize_password_reset_token,
                                          _serialize_verification_token,
                                          create_fresh_user_access_token,
                                          create_user_refresh_token)
from tests.components.auth.helpers import (get_mock_email_body,
                                           get_mock_email_password_body,
                                           get_mock_password_body,
                                           get_mock_sign_up_body)
from tests.helpers import TestBase, fake


class TestAuth(TestBase):

    #
    # sign_up_POST tests.
    #

    @patch("dawdle.components.auth.blueprints.send_verification_email")
    @patch("dawdle.components.auth.blueprints.save_new_user")
    def test_sign_up_POST_201(self, save_new_user, send_verification_email):
        user = self._create_user(active=False)
        save_new_user.return_value = user
        body = get_mock_sign_up_body()
        response = self.__send_sign_up_POST_request(body)
        self._assert_201(response)
        save_new_user.assert_called_with(
            body["name"],
            body["email"],
            body["password"],
        )
        send_verification_email.assert_called_with(user)

    def test_sign_up_POST_400_bad_data(self):
        body = get_mock_sign_up_body()
        del body["name"]
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "name": [
                "Missing data for required field.",
            ],
        })

    def test_sign_up_POST_400_existing(self):
        body = get_mock_sign_up_body(email=self._user.email)
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "email": [
                "There is already an account with this email.",
            ],
        })

    def test_sign_up_POST_415(self):
        response = self._client.post(url_for("auth.sign_up_POST"))
        self._assert_415(response)

    def __send_sign_up_POST_request(self, body):
        return self._client.post(
            url_for("auth.sign_up_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )

    #
    # verify_POST tests.
    #

    @patch("dawdle.components.auth.blueprints.send_verification_email")
    def test_verify_POST_204(self, send_verification_email):
        user = self._create_user(active=False)
        body = get_mock_email_body(email=user.email)
        response = self.__send_verify_POST_request(body)
        self._assert_204(response)
        send_verification_email.assert_called_with(user)

    def test_verify_POST_400_bad_data(self):
        body = get_mock_email_body()
        del body["email"]
        response = self.__send_verify_POST_request(body)
        self._assert_400(response, {
            "email": [
                "Missing data for required field.",
            ],
        })

    def test_verify_POST_400_verified(self):
        body = get_mock_email_body(email=self._user.email)
        response = self.__send_verify_POST_request(body)
        self._assert_400(response, {
            "email": [
                "This email has already been verified.",
            ],
        })

    def test_verify_POST_404(self):
        body = get_mock_email_body()
        response = self.__send_verify_POST_request(body)
        self._assert_404(response)

    def test_verify_POST_415(self):
        response = self._client.post(url_for("auth.verify_POST"))
        self._assert_415(response)

    def __send_verify_POST_request(self, body):
        return self._client.post(
            url_for("auth.verify_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )

    #
    # verify_token_POST tests.
    #

    @patch("dawdle.components.auth.blueprints.activate_user")
    def test_verify_token_POST_204(self, activate_user):
        user = self._create_user(active=False)
        token = _serialize_verification_token(user)
        response = self.__send_verify_token_POST_request(token)
        self._assert_204(response)
        activate_user.assert_called_with(user)

    def test_verify_token_POST_400(self):
        response = self.__send_verify_token_POST_request("token")
        self._assert_400(response, {
            "token": [
                "Invalid token.",
            ],
        })

    def __send_verify_token_POST_request(self, token):
        return self._client.post(
            url_for("auth.verify_token_POST", token=token),
        )

    #
    # token_POST tests.
    #

    def test_token_POST_200(self):
        body = get_mock_email_password_body(
            email=self._user.email,
            password=self._password,
        )
        response = self.__send_token_POST_request(body)
        self._assert_200(response)
        assert "access_token" in response.json
        assert "refresh_token" in response.json
        assert response.json["user_id"] == str(self._user.id)

    def test_token_POST_400_bad_data(self):
        body = get_mock_email_password_body()
        del body["email"]
        response = self.__send_token_POST_request(body)
        self._assert_400(response, {
            "email": [
                "Missing data for required field.",
            ],
        })

    def test_token_POST_400_wrong_password(self):
        body = get_mock_email_password_body(email=self._user.email)
        response = self.__send_token_POST_request(body)
        self._assert_400(response, {
            "password": [
                "Incorrect password.",
            ],
        })

    def test_token_POST_400_not_verified(self):
        user = self._create_user(active=False, password=self._password)
        body = get_mock_email_password_body(
            email=user.email,
            password=self._password,
        )
        response = self.__send_token_POST_request(body)
        self._assert_400(response, {
            "email": [
                "This email has not been verified.",
            ],
        })

    def test_token_POST_404(self):
        body = get_mock_email_password_body()
        response = self.__send_token_POST_request(body)
        self._assert_404(response)

    def test_token_POST_415(self):
        response = self._client.post(url_for("auth.token_POST"))
        self._assert_415(response)

    def __send_token_POST_request(self, body):
        return self._client.post(
            url_for("auth.token_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )

    #
    # token_refresh_GET tests.
    #

    def test_token_refresh_GET_200(self):
        response = self.__send_token_refresh_GET_request(self._refresh_token)
        self._assert_200(response)
        assert "access_token" in response.json
        assert "refresh_token" not in response.json
        assert response.json["user_id"] == str(self._user.id)

    def test_token_refresh_GET_400_bad_token(self):
        response = self.__send_token_refresh_GET_request("invalid")
        self._assert_400(response, {
            "token": [
                "Invalid token.",
            ],
        })

    def test_token_refresh_GET_400_not_existing(self):
        user = self._create_user()
        token = create_user_refresh_token(user)
        user.delete()
        response = self.__send_token_refresh_GET_request(token)
        self._assert_400(response, {
            "token": [
                "Invalid token.",
            ],
        })

    def test_token_refresh_GET_401(self):
        response = self.__send_token_refresh_GET_request()
        self._assert_401(response)

    def __send_token_refresh_GET_request(self, token=None):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return self._client.get(
            url_for("auth.token_refresh_GET"),
            headers=headers,
        )

    #
    # reset_password_POST tests.
    #

    @patch("dawdle.components.auth.blueprints.send_password_reset_email")
    def test_reset_password_POST_204(self, send_password_reset_email):
        body = get_mock_email_body(email=self._user.email)
        response = self.__send_reset_password_POST_request(body)
        self._assert_204(response)
        send_password_reset_email.assert_called_with(self._user)

    def test_reset_password_POST_400(self):
        body = get_mock_email_body()
        del body["email"]
        response = self.__send_reset_password_POST_request(body)
        self._assert_400(response, {
            "email": [
                "Missing data for required field.",
            ],
        })

    def test_reset_password_POST_404(self):
        body = get_mock_email_body()
        response = self.__send_reset_password_POST_request(body)
        self._assert_404(response)

    def test_reset_password_POST_415(self):
        response = self._client.post(
            url_for("auth.reset_password_POST"),
        )
        self._assert_415(response)

    def __send_reset_password_POST_request(self, body):
        return self._client.post(
            url_for("auth.reset_password_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )

    #
    # reset_password_token_POST tests.
    #

    @patch("dawdle.components.auth.blueprints.update_user_password")
    def test_reset_password_token_POST_204(self, update_user_password):
        token = _serialize_password_reset_token(self._user)
        password = fake.password()
        body = get_mock_password_body(password=password)
        response = self.__send_reset_password_token_POST_request(token, body)
        self._assert_204(response)
        update_user_password.assert_called_with(self._user, password)

    def test_reset_password_token_POST_400_bad_data(self):
        token = _serialize_password_reset_token(self._user)
        body = get_mock_password_body()
        del body["password"]
        response = self.__send_reset_password_token_POST_request(token, body)
        self._assert_400(response, {
            "password": [
                "Missing data for required field.",
            ],
        })

    def test_reset_password_token_POST_400_bad_token(self):
        response = self.__send_reset_password_token_POST_request(
            "token",
            get_mock_password_body(),
        )
        self._assert_400(response, {
            "token": [
                "Invalid token.",
            ],
        })

    def test_reset_password_token_POST_415(self):
        response = self._client.post(
            url_for("auth.reset_password_token_POST", token="token"),
        )
        self._assert_415(response)

    def __send_reset_password_token_POST_request(self, token, body):
        return self._client.post(
            url_for("auth.reset_password_token_POST", token=token),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )

    #
    # users_user_password_POST tests.
    #

    @patch("dawdle.components.auth.blueprints.update_user_password")
    def test_users_user_password_POST_204(self, update_user_password):
        password = fake.password()
        body = get_mock_password_body(password=password)
        response = self.__send_users_user_password_POST_request(
            self._user.id,
            body,
            self._fresh_access_token,
        )
        self._assert_204(response)
        update_user_password.assert_called_with(self._user, password)

    def test_users_user_password_POST_400_not_fresh_token(self):
        response = self.__send_users_user_password_POST_request(
            self._user.id,
            get_mock_password_body(),
            self._access_token,
        )
        self._assert_400(response, {
            "token": [
                "Needs fresh token.",
            ],
        })

    def test_users_user_password_POST_400_bad_data(self):
        body = get_mock_password_body()
        del body["password"]
        response = self.__send_users_user_password_POST_request(
            self._user.id,
            body,
            self._fresh_access_token,
        )
        self._assert_400(response, {
            "password": [
                "Missing data for required field.",
            ],
        })

    def test_users_user_password_POST_401(self):
        response = self.__send_users_user_password_POST_request(
            self._user.id,
            get_mock_password_body(),
        )
        self._assert_401(response)

    def test_users_user_password_POST_403(self):
        response = self.__send_users_user_password_POST_request(
            self._create_user().id,
            get_mock_password_body(),
            self._fresh_access_token,
        )
        self._assert_403(response)

    def test_users_user_password_POST_404(self):
        user = self._create_user()
        token = create_fresh_user_access_token(user)
        user.delete()
        response = self.__send_users_user_password_POST_request(
            user.id,
            get_mock_password_body(),
            token,
        )
        self._assert_404(response)

    def test_users_user_password_POST_415(self):
        response = self._client.post(
            url_for("auth.users_user_password_POST", user_id=self._user.id),
        )
        self._assert_415(response)

    def __send_users_user_password_POST_request(self,
                                                user_id,
                                                body,
                                                token=None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        return self._client.post(
            url_for("auth.users_user_password_POST", user_id=user_id),
            headers=headers,
            data=json.dumps(body),
        )
