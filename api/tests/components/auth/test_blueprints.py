import json
from unittest.mock import patch

from flask import url_for
from flask_jwt_extended import create_refresh_token

from dawdle.components.auth.utils import (get_user_by_email,
                                          serialize_password_reset_token,
                                          serialize_verification_token,
                                          verify_password)
from tests.components.auth.helpers import (get_mock_email_body,
                                           get_mock_email_password_body,
                                           get_mock_password_body,
                                           get_mock_sign_up_body)
from tests.helpers import TestBase, fake


class TestAuth(TestBase):

    #
    # sign_up_POST tests.
    #

    def test_sign_up_POST_201(self):
        body = get_mock_sign_up_body()
        response = self.__send_sign_up_POST_request(body)
        self._assert_201(response)
        user = get_user_by_email(body["email"])
        assert user.email == body["email"]
        assert user.initials
        assert user.name == body["name"].strip()
        assert verify_password(user.password, body["password"])

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
        body = get_mock_sign_up_body(email=self.user.email)
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "email": [
                "There is already an account with this email.",
            ],
        })

    def test_sign_up_POST_415(self):
        response = self.client.post(url_for("auth.sign_up_POST"))
        self._assert_415(response)

    def __send_sign_up_POST_request(self, body):
        return self.client.post(
            url_for("auth.sign_up_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )

    #
    # verify_POST tests.
    #

    @patch("dawdle.components.auth.blueprints.send_verification_email")
    def test_verify_POST_204(self, send_verification_email):
        user = self.create_user(active=False)
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

    def test_verify_POST_400_not_existing(self):
        body = get_mock_email_body()
        response = self.__send_verify_POST_request(body)
        self._assert_400(response, {
            "email": [
                "There is no account with this email.",
            ],
        })

    def test_verify_POST_400_verified(self):
        body = get_mock_email_body(email=self.user.email)
        response = self.__send_verify_POST_request(body)
        self._assert_400(response, {
            "email": [
                "This email has already been verified.",
            ],
        })

    def test_verify_POST_415(self):
        response = self.client.post(url_for("auth.verify_POST"))
        self._assert_415(response)

    def __send_verify_POST_request(self, body):
        return self.client.post(
            url_for("auth.verify_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )

    #
    # verify_GET tests.
    #

    def test_verify_GET_204(self):
        user = self.create_user(active=False)
        token = serialize_verification_token(user)
        response = self.__send_verify_GET_request(token)
        self._assert_204(response)
        updated_user = get_user_by_email(user.email)
        assert updated_user.active
        assert updated_user.auth_id != user.auth_id
        assert updated_user.last_updated != user.last_updated
        assert updated_user.updated_by == updated_user

    def test_verify_GET_400(self):
        response = self.__send_verify_GET_request("token")
        self._assert_400(response, {
            "token": [
                "Invalid token.",
            ],
        })

    def __send_verify_GET_request(self, token):
        return self.client.get(url_for("auth.verify_GET", token=token))

    #
    # token_POST tests.
    #

    def test_token_POST_200(self):
        body = get_mock_email_password_body(
            email=self.user.email,
            password=self.password,
        )
        response = self.__send_token_POST_request(body)
        self._assert_200(response)
        assert "access_token" in response.json
        assert "refresh_token" in response.json
        assert response.json["user_id"] == str(self.user.id)

    def test_token_POST_400_bad_data(self):
        body = get_mock_email_password_body()
        del body["email"]
        response = self.__send_token_POST_request(body)
        self._assert_400(response, {
            "email": [
                "Missing data for required field.",
            ],
        })

    def test_token_POST_400_not_existing(self):
        body = get_mock_email_password_body()
        response = self.__send_token_POST_request(body)
        self._assert_400(response, {
            "email": [
                "Incorrect email.",
            ],
            "password": [
                "Incorrect password.",
            ],
        })

    def test_token_POST_400_wrong_password(self):
        body = get_mock_email_password_body(email=self.user.email)
        response = self.__send_token_POST_request(body)
        self._assert_400(response, {
            "email": [
                "Incorrect email.",
            ],
            "password": [
                "Incorrect password.",
            ],
        })

    def test_token_POST_400_not_verified(self):
        user = self.create_user(active=False, password=self.password)
        body = get_mock_email_password_body(
            email=user.email,
            password=self.password,
        )
        response = self.__send_token_POST_request(body)
        self._assert_400(response, {
            "email": [
                "This email has not been verified.",
            ],
        })

    def test_token_POST_415(self):
        response = self.client.post(url_for("auth.token_POST"))
        self._assert_415(response)

    def __send_token_POST_request(self, body):
        return self.client.post(
            url_for("auth.token_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )

    #
    # token_refresh_GET tests.
    #

    def test_token_refresh_GET_200(self):
        token = create_refresh_token(str(self.user.auth_id))
        response = self.__send_token_refresh_GET_request(token)
        self._assert_200(response)
        assert "access_token" in response.json
        assert "refresh_token" not in response.json
        assert response.json["user_id"] == str(self.user.id)

    def test_token_refresh_GET_400(self):
        response = self.__send_token_refresh_GET_request("invalid")
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
        return self.client.get(
            url_for("auth.token_refresh_GET"),
            headers=headers,
        )

    #
    # reset_password_request_POST tests.
    #

    @patch("dawdle.components.auth.blueprints.send_password_reset_email")
    def test_reset_password_request_POST_204(self, send_password_reset_email):
        body = get_mock_email_body(email=self.user.email)
        response = self.__send_reset_password_request_POST_request(body)
        self._assert_204(response)
        send_password_reset_email.assert_called_with(self.user)

    def test_reset_password_request_POST_400_bad_data(self):
        body = get_mock_email_body()
        del body["email"]
        response = self.__send_reset_password_request_POST_request(body)
        self._assert_400(response, {
            "email": [
                "Missing data for required field.",
            ],
        })

    def test_reset_password_request_POST_400_not_existing(self):
        body = get_mock_email_body()
        response = self.__send_reset_password_request_POST_request(body)
        self._assert_400(response, {
            "email": [
                "There is no account with this email.",
            ],
        })

    def test_reset_password_request_POST_415(self):
        response = self.client.post(
            url_for("auth.reset_password_request_POST"),
        )
        self._assert_415(response)

    def __send_reset_password_request_POST_request(self, body):
        return self.client.post(
            url_for("auth.reset_password_request_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )

    #
    # reset_password_POST tests.
    #

    def test_reset_password_POST_204(self):
        user = self.create_user()
        token = serialize_password_reset_token(user)
        password = fake.password()
        body = get_mock_password_body(password=password)
        response = self.__send_reset_password_POST_request(token, body)
        self._assert_204(response)
        updated_user = get_user_by_email(user.email)
        assert updated_user.auth_id != user.auth_id
        assert updated_user.last_updated != user.last_updated
        assert verify_password(updated_user.password, password)
        assert updated_user.updated_by == updated_user

    def test_reset_password_POST_400_bad_token(self):
        response = self.__send_reset_password_POST_request(
            "token",
            get_mock_password_body(),
        )
        self._assert_400(response, {
            "token": [
                "Invalid token.",
            ],
        })

    def test_reset_password_POST_400_bad_data(self):
        token = serialize_password_reset_token(self.user)
        body = get_mock_password_body()
        del body["password"]
        response = self.__send_reset_password_POST_request(token, body)
        self._assert_400(response, {
            "password": [
                "Missing data for required field.",
            ],
        })

    def test_reset_password_POST_415(self):
        response = self.client.post(
            url_for("auth.reset_password_POST", token="token"),
        )
        self._assert_415(response)

    def __send_reset_password_POST_request(self, token, body):
        return self.client.post(
            url_for("auth.reset_password_POST", token=token),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )
