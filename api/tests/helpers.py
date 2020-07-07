from faker import Faker

from dawdle import create_app
from dawdle.components.auth.utils import encrypt_password
from dawdle.components.user.models import User
from dawdle.utils.schemas import Limits

fake = Faker()


class TestBase:

    @classmethod
    def setup_class(cls):
        cls.app = create_app(testing=True)
        cls.app.app_context().push()
        cls.client = cls.app.test_client()

        cls.password = fake.password()
        cls.user = cls.create_user(password=cls.password)

    @classmethod
    def create_user(cls, **kwargs):
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
        cls.clear_db()

    @classmethod
    def clear_db(cls):
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
