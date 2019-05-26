from faker import Faker

from dawdle import create_app
from dawdle.models.user import User

fake = Faker()

class TestBase:

    def setup_method(self):
        # set up test app instance
        self.app = create_app(testing=True)
        self.client = self.app.test_client()

        # set up a test user and login
        self.password = fake.password()
        self.user = self.create_user(password=self.password)
        self.login(self.user.email, self.password)

    def create_user(self,
                    active=True,
                    email=fake.email,
                    name=fake.name,
                    password=fake.password):
        user = User()
        user.active = active
        user.email = email() if callable(email) else email
        user.name = name() if callable(name) else name
        user.password = User.encrypt_password(password() if callable(password) else password)
        return user.save()

    def login(self, email, password):
        self.client.post('/auth/login', data={'email': email, 'password': password})

    def get_random_string(self, length):
        return fake.sentence(nb_words=length)[:length]

    def teardown_method(self):
        self.logout()
        self.clear_db()

    def logout(self):
        self.client.get('/auth/logout')

    def clear_db(self):
        User.objects.delete()
