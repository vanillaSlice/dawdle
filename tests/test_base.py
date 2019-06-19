from faker import Faker
from flask import url_for

from dawdle import create_app
from dawdle.models.user import User

class TestBase:

    @classmethod
    def setup_class(cls):
        cls.fake = Faker()

        cls.app = create_app(testing=True)
        cls.app.app_context().push()
        cls.client = cls.app.test_client()

        cls.password = cls.fake.password()
        cls.user = cls.create_user(password=cls.password)
        cls.login()

    @classmethod
    def teardown_class(cls):
        cls.clear_db()

    @classmethod
    def create_user(cls, **kwargs):
        user = User()
        user.active = kwargs.get('active', True)
        user.email = kwargs.get('email', cls.fake.email())
        user.initials = kwargs.get('initials', cls.fake.pystr(min_chars=1, max_chars=4))
        user.name = kwargs.get('name', cls.fake.name())
        user.password = User.encrypt_password(kwargs.get('password', cls.fake.password()))
        return user.save()

    @classmethod
    def as_new_user(cls):
        password = cls.fake.password()
        user = cls.create_user(active=True, password=password)
        cls.login(email=user.email, password=password)
        return user, password

    @classmethod
    def login(cls, **kwargs):
        email = kwargs.get('email', cls.user.email)
        password = kwargs.get('password', cls.password)
        cls.client.post(url_for('auth.login_POST'), data={'email': email, 'password': password})
        cls.logged_in = cls.user.email == email and cls.password == password

    @classmethod
    def logout(cls):
        cls.client.get(url_for('auth.logout_GET'))
        cls.logged_in = False

    @classmethod
    def clear_db(cls):
        User.objects.delete()

    def setup_method(self):
        if not self.logged_in:
            self.login()
