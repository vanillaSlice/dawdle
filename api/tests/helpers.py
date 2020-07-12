from faker import Faker
from werkzeug import exceptions
from werkzeug.http import HTTP_STATUS_CODES

from dawdle import create_app
from dawdle.components.auth.utils import (create_fresh_user_access_token,
                                          create_user_access_token,
                                          create_user_refresh_token,
                                          encrypt_password)
from dawdle.components.users.models import User
from dawdle.extensions.marshmallow import Limits

fake = Faker()


class TestBase:

    @classmethod
    def setup_class(cls):
        cls._app = create_app(testing=True)
        cls._app.app_context().push()
        cls._client = cls._app.test_client()

        cls._password = fake.password()
        cls._user = cls._create_user(password=cls._password)
        cls._fresh_access_token = create_fresh_user_access_token(cls._user)
        cls._access_token = create_user_access_token(cls._user)
        cls._refresh_token = create_user_refresh_token(cls._user)

    @classmethod
    def _create_user(cls, **kwargs):
        user = User()
        user.active = kwargs.get("active", True)
        user.email = kwargs.get("email", fake.email())
        user.initials = kwargs.get(
            "initials",
            fake.pystr(max_chars=Limits.MAX_USER_INITIALS_LENGTH),
        ).upper()
        user.name = kwargs.get("name", fake.name())
        user.password = encrypt_password(
            kwargs.get("password", fake.password()),
        )
        return user.save()

    @classmethod
    def teardown_class(cls):
        cls.__clear_db()

    @classmethod
    def __clear_db(cls):
        User.objects.delete()

    @staticmethod
    def __assert_response(response, status, body=None):
        assert response.status_code == status
        if body:
            assert response.json == body

    def _assert_200(self, response, body=None):
        self.__assert_response(response, 200, body)

    def _assert_201(self, response, body=None):
        self.__assert_response(response, 201, body)

    def _assert_204(self, response, body=None):
        self.__assert_response(response, 204, body)

    def __assert_error(self, response, exception, messages=None):
        body = {
            "status": exception.code,
            "name": HTTP_STATUS_CODES[exception.code],
            "description": exception.description,
            "messages": messages if messages else {},
        }
        self.__assert_response(response, exception.code, body)

    def _assert_400(self, response, messages=None):
        self.__assert_error(response, exceptions.BadRequest(), messages)

    def _assert_401(self, response, messages=None):
        self.__assert_error(response, exceptions.Unauthorized(), messages)

    def _assert_403(self, response, messages=None):
        self.__assert_error(response, exceptions.Forbidden(), messages)

    def _assert_404(self, response, messages=None):
        self.__assert_error(response, exceptions.NotFound(), messages)

    def _assert_415(self, response, messages=None):
        self.__assert_error(
            response,
            exceptions.UnsupportedMediaType(),
            messages,
        )

    def _assert_500(self, response, messages=None):
        self.__assert_error(
            response,
            exceptions.InternalServerError(),
            messages,
        )
