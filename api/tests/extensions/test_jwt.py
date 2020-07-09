import datetime

from flask import url_for
from flask_jwt_extended import create_refresh_token

from tests.helpers import TestBase, fake


class TestJtw(TestBase):

    def test_400_expired(self):
        token = create_refresh_token(
            str(self._user.auth_id),
            expires_delta=datetime.timedelta(hours=-12),
        )
        response = self.__send_request(token)
        self._assert_400(response, {
            "token": [
                "Token expired.",
            ],
        })

    def test_400_invalid(self):
        response = self.__send_request(fake.sentence())
        self._assert_400(response, {
            "token": [
                "Invalid token.",
            ],
        })

    def test_401(self):
        response = self.__send_request()
        self._assert_401(response)

    def __send_request(self, token=None):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return self._client.get(
            url_for("auth.token_refresh_GET"),
            headers=headers,
        )
