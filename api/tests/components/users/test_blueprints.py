from flask import url_for

from dawdle.components.auth.utils import create_user_access_token
from dawdle.components.users.schemas import user_schema
from tests.helpers import TestBase


class TestUsers(TestBase):

    def test_users_user_info_GET_200(self):
        response = self.__send_users_user_info_GET_request(
            self._user.id,
            self._access_token,
        )
        self._assert_200(response, user_schema.dump({
            "created": self._user.created,
            "email": self._user.email,
            "initials": self._user.initials,
            "name": self._user.name,
        }))

    def test_users_user_info_GET_400(self):
        response = self.__send_users_user_info_GET_request(
            self._create_user().id,
            self._refresh_token,
        )
        self._assert_400(response, {
            "token": [
                "Invalid token.",
            ],
        })

    def test_users_user_info_GET_401(self):
        response = self.__send_users_user_info_GET_request(self._user.id)
        self._assert_401(response)

    def test_users_user_info_GET_403(self):
        response = self.__send_users_user_info_GET_request(
            self._create_user().id,
            self._access_token,
        )
        self._assert_403(response)

    def test_users_user_info_GET_404(self):
        user = self._create_user()
        token = create_user_access_token(user)
        user.delete()
        response = self.__send_users_user_info_GET_request(user.id, token)
        self._assert_404(response)

    def __send_users_user_info_GET_request(self, user_id, token=None):
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        return self._client.get(
            url_for("users.users_user_info_GET", user_id=user_id),
            headers=headers,
        )
