from faker import Faker
from flask_jwt_extended import create_access_token, create_refresh_token

from dawdle import create_app
from dawdle.components.auth.utils import encrypt_password
from dawdle.components.user.models import User
from dawdle.utils.schemas import Limits

fake = Faker()


class TestBase:

    @classmethod
    def setup_class(cls):
        cls._app = create_app(testing=True)
        cls._app.app_context().push()
        cls._client = cls._app.test_client()

        cls._password = fake.password()
        cls._user = cls._create_user(password=cls._password)
        cls._identity = str(cls._user.auth_id)
        cls._fresh_access_token = create_access_token(
            identity=cls._identity,
            fresh=True,
        )
        cls._access_token = create_access_token(identity=cls._identity)
        cls._refresh_token = create_refresh_token(identity=cls._identity)

    @classmethod
    def _create_user(cls, **kwargs):
        user = User()
        user.active = kwargs.get("active", True)
        user.email = kwargs.get("email", fake.email())
        user.initials = kwargs.get(
            "initials",
            fake.pystr(Limits.MAX_USER_INITIALS_LENGTH),
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
    def _assert_response(response, status, body=None):
        assert response.status_code == status
        if body:
            assert response.json == body

    def _assert_200(self, response, body=None):
        self._assert_response(response, 200, body)

    def _assert_201(self, response, body=None):
        self._assert_response(response, 201, body)

    def _assert_204(self, response, body=None):
        self._assert_response(response, 204, body)

    def _assert_error(self,
                      response,
                      status,
                      name,
                      description,
                      messages=None):
        body = {
            "status": status,
            "name": name,
            "description": description,
            "messages": messages if messages else {},
        }
        self._assert_response(response, status, body)

    def _assert_400(self, response, messages=None):
        self._assert_error(
            response,
            400,
            "Bad Request",
            "The browser (or proxy) sent a request that this server could not "
            "understand.",
            messages,
        )

    def _assert_401(self, response, messages=None):
        self._assert_error(
            response,
            401,
            "Unauthorized",
            "The server could not verify that you are authorized to access "
            "the URL requested. You either supplied the wrong credentials "
            "(e.g. a bad password), or your browser doesn't understand how "
            "to supply the credentials required.",
            messages,
        )

    def _assert_403(self, response, messages=None):
        self._assert_error(
            response,
            403,
            "Forbidden",
            "You don't have the permission to access the requested resource. "
            "It is either read-protected or not readable by the server.",
            messages,
        )

    def _assert_415(self, response):
        self._assert_error(
            response,
            415,
            "Unsupported Media Type",
            "The server does not support the media type transmitted in the "
            "request.",
        )

    def _assert_500(self, response):
        self._assert_error(
            response,
            500,
            "Internal Server Error",
            "The server encountered an internal error and was unable to "
            "complete your request. Either the server is overloaded or "
            "there is an error in the application.",
        )
