from faker import Faker

from dawdle import create_app
from dawdle.components.auth.utils import encrypt_password
from dawdle.components.user.models import User


class TestBlueprint:

    @classmethod
    def setup_class(cls):
        cls.fake = Faker()

        cls.app = create_app(testing=True)
        cls.app.app_context().push()
        cls.client = cls.app.test_client()

        cls.password = cls.fake.password()
        cls.user = cls.create_user(password=cls.password)

    @classmethod
    def create_user(cls, **kwargs):
        user = User()
        user.active = kwargs.get("active", True)
        user.email = kwargs.get("email", cls.fake.email())
        user.initials = kwargs.get(
            "initials",
            cls.fake.pystr(min_chars=1, max_chars=4).upper(),
        ).upper()
        user.name = kwargs.get("name", cls.fake.name())
        user.password = encrypt_password(
            kwargs.get("password", cls.fake.password()),
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

    def _assert_201(self, response, body=None):
        self._assert_response(response, 201, body)

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

    def _assert_404(self, response):
        self._assert_error(
            response,
            404,
            "Not Found",
            "The requested URL was not found on the server. If you entered "
            "the URL manually please check your spelling and try again.",
        )

    def _assert_415(self, response):
        self._assert_error(
            response,
            415,
            "Unsupported Media Type",
            "The server does not support the media type transmitted in the "
            "request.",
        )
