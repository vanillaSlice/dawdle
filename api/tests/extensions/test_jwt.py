import datetime

from bson.objectid import ObjectId
from flask import url_for
from flask_jwt_extended import create_refresh_token

from tests.utils import TestBase, fake


class TestJtw(TestBase):

    def test_400_expired(self):
        token = create_refresh_token(
            str(self.user.auth_id),
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

    def test_400_not_existing(self):
        response = self.__send_request(str(ObjectId()))
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
        return self.client.get(
            url_for("auth.token_refresh_GET"),
            headers=headers,
        )
