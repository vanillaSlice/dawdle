import json

from flask import url_for

from dawdle.components.auth.utils import verify_password
from dawdle.components.user.utils import get_user_by_email
from tests.helpers import TestBlueprint


class TestAuth(TestBlueprint):

    #
    # sign_up_POST tests.
    #

    def test_sign_up_POST_success(self):
        body = self.__get_mock_sign_up_body()
        self.__assert_sign_up_POST_ok(body)

    def test_sign_up_POST_no_name(self):
        body = self.__get_mock_sign_up_body()
        del body["name"]
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "name": [
                "Missing data for required field.",
            ],
        })

    def test_sign_up_POST_blank_name(self):
        body = self.__get_mock_sign_up_body(name="     ")
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "name": [
                "Missing data for required field.",
            ],
        })

    def test_sign_up_POST_name_equal_to_min(self):
        name = self.fake.pystr(min_chars=1, max_chars=1)
        body = self.__get_mock_sign_up_body(name=name)
        self.__assert_sign_up_POST_ok(body)

    def test_sign_up_POST_name_equal_to_max(self):
        name = self.fake.pystr(min_chars=50, max_chars=50)
        body = self.__get_mock_sign_up_body(name=name)
        self.__assert_sign_up_POST_ok(body)

    def test_sign_up_POST_name_greater_than_max(self):
        name = self.fake.pystr(min_chars=51, max_chars=51)
        body = self.__get_mock_sign_up_body(name=name)
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "name": [
                "Length must be between 1 and 50.",
            ],
        })

    def test_sign_up_POST_trims_name(self):
        body = self.__get_mock_sign_up_body(name="  John   ")
        self.__assert_sign_up_POST_ok(body)

    def test_sign_up_POST_no_email(self):
        body = self.__get_mock_sign_up_body()
        del body["email"]
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "email": [
                "Missing data for required field.",
            ],
        })

    def test_sign_up_POST_invalid_email(self):
        email = self.fake.sentence()
        body = self.__get_mock_sign_up_body(email=email)
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "email": [
                "Not a valid email address.",
            ],
        })

    def test_sign_up_POST_no_password(self):
        body = self.__get_mock_sign_up_body()
        del body["password"]
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "password": [
                "Missing data for required field.",
            ],
        })

    def test_sign_up_POST_password_less_than_min(self):
        password = self.fake.pystr(min_chars=1, max_chars=7)
        body = self.__get_mock_sign_up_body(password=password)
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "password": [
                "Shorter than minimum length 8.",
            ],
        })

    def test_sign_up_POST_password_equal_to_min(self):
        password = self.fake.pystr(min_chars=8, max_chars=8)
        body = self.__get_mock_sign_up_body(password=password)
        self.__assert_sign_up_POST_ok(body)

    def test_sign_up_POST_account_already_exists(self):
        email = self.user.email
        body = self.__get_mock_sign_up_body(email=email)
        response = self.__send_sign_up_POST_request(body)
        self._assert_400(response, {
            "email": [
                "There is already an account with this email.",
            ],
        })

    def test_sign_up_POST_method_not_found(self):
        response = self.client.get(url_for("auth.sign_up_POST"))
        self._assert_404(response)

    def test_sign_up_POST_unsupported_media_type(self):
        response = self.client.post(url_for("auth.sign_up_POST"))
        self._assert_415(response)

    def __get_mock_sign_up_body(self, **kwargs):
        return {
            "email": kwargs.get("email", self.fake.email()),
            "name": kwargs.get("name", self.fake.name()),
            "password": kwargs.get("password", self.fake.password()),
        }

    def __send_sign_up_POST_request(self, body):
        return self.client.post(
            url_for("auth.sign_up_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )

    def __assert_sign_up_POST_ok(self, body):
        response = self.__send_sign_up_POST_request(body)
        self._assert_201(response)
        user = get_user_by_email(body["email"])
        assert user.name == body["name"].strip()
        assert verify_password(user, body["password"])
        assert user.initials
