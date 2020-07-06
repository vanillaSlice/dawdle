import json

from flask import url_for

from dawdle.components.auth.utils import verify_password
from dawdle.components.user.utils import get_user_by_email
from tests.components.auth.utils import get_mock_sign_up_body
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

    def test_sign_up_POST_404(self):
        response = self.client.get(url_for("auth.sign_up_POST"))
        self._assert_404(response)

    def test_sign_up_POST_415(self):
        response = self.client.post(url_for("auth.sign_up_POST"))
        self._assert_415(response)

    def __send_sign_up_POST_request(self, body):
        return self.client.post(
            url_for("auth.sign_up_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )
