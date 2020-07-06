import json
from unittest.mock import patch

from flask import url_for
from itsdangerous import URLSafeSerializer

from dawdle.components.auth.utils import (serialize_verification_token,
                                          verify_password)
from dawdle.components.user.utils import get_user_by_email
from dawdle.extensions.sendgrid import TEMPLATE_IDS
from tests.components.auth.utils import (get_mock_email_body,
                                         get_mock_email_password_body,
                                         get_mock_sign_up_body)
from tests.utils import TestBlueprint


class TestAuth(TestBlueprint):

    #
    # sign_up_POST tests.
    #

    def test_sign_up_POST_201(self):
        body = get_mock_sign_up_body()
        response = self.__send_sign_up_POST_request(body)
        self._assert_201(response)
        user = get_user_by_email(body["email"])
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
        email = self.user.email
        body = get_mock_sign_up_body(email=email)
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

    @patch("dawdle.components.auth.utils.sendgrid")
    def test_verify_POST_204(self, sendgrid):
        user = self.create_user(active=False)
        body = get_mock_email_body(email=user.email)
        response = self.__send_verify_POST_request(body)
        self._assert_204(response)
        sendgrid.send.assert_called_with(
            TEMPLATE_IDS["verification"],
            user.email,
            data={
                "name": user.name,
                "token": serialize_verification_token(user),
            }
        )

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
        token = self.__get_verify_token(str(user.auth_id))
        response = self.__send_verify_GET_request(token)
        self._assert_204(response)
        updated_user = get_user_by_email(user.email)
        assert updated_user.active
        assert updated_user.auth_id != user.auth_id
        assert updated_user.last_updated != user.last_updated

    def test_verify_GET_400_bad_token(self):
        response = self.__send_verify_GET_request("token")
        self._assert_400(response, {
            "token": [
                "Invalid token.",
            ],
        })

    def test_verify_GET_400_bad_auth_id(self):
        token = self.__get_verify_token("some token")
        response = self.__send_verify_GET_request(token)
        self._assert_400(response, {
            "token": [
                "Invalid token.",
            ],
        })

    def __get_verify_token(self, auth_id):
        return URLSafeSerializer(self.app.secret_key).dumps(auth_id)

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
