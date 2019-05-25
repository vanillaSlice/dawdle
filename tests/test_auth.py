from dawdle.models.user import User
from tests.test_base import fake, TestBase

class TestAuth(TestBase):

    #
    # Utils
    #

    def get_mock_sign_up_data(self,
                              email=fake.email(),
                              name=fake.name(),
                              password=fake.password()):
        return {
            'email': email,
            'name': name,
            'password': password,
        }

    #
    # /auth/sign-up Tests.
    #

    def assert_sign_up_successful(self, data):
        response = self.client.post('/auth/sign-up', data=data)
        user = User.objects(email=data['email']).first()
        assert response.status_code == 302
        assert user.is_active is False
        assert user.name == data['name']
        assert user.verify_password(data['password']) is True

    def assert_sign_up_unsuccessful(self, data):
        response = self.client.post('/auth/sign-up', data=data)
        user = User.objects(email=data['email']).first()
        assert response.status_code == 400
        assert len(User.objects()) == 1

    def test_sign_up_GET(self):
        response = self.client.get('/auth/sign-up')
        assert response.status_code == 200

    def test_sign_up_no_name(self):
        name = None
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_unsuccessful(data)

    def test_sign_up_name_length_equal_to_minimum(self):
        name = self.get_random_string(length=1)
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_successful(data)

    def test_sign_up_name_length_equal_to_maximum(self):
        name = self.get_random_string(length=50)
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_successful(data)

    def test_sign_up_name_length_greater_than_maximum(self):
        name = self.get_random_string(length=51)
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_unsuccessful(data)

    def test_sign_up_no_email(self):
        email = None
        data = self.get_mock_sign_up_data(email=email)
        self.assert_sign_up_unsuccessful(data)

    def test_sign_up_invalid_email(self):
        email = fake.sentence()
        data = self.get_mock_sign_up_data(email=email)
        self.assert_sign_up_unsuccessful(data)

    def test_sign_up_no_password(self):
        password = None
        data = self.get_mock_sign_up_data(password=password)
        self.assert_sign_up_unsuccessful(data)

    def test_sign_up_password_length_less_than_minimum(self):
        password = self.get_random_string(length=7)
        data = self.get_mock_sign_up_data(password=password)
        self.assert_sign_up_unsuccessful(data)

    def test_sign_up_password_length_equal_to_minimum(self):
        password = self.get_random_string(length=8)
        data = self.get_mock_sign_up_data(password=password)
        self.assert_sign_up_successful(data)

    def test_sign_up_account_already_exists(self):
        email = self.user.email
        data = self.get_mock_sign_up_data(email=email)
        self.assert_sign_up_unsuccessful(data)

    def test_sign_up_success(self):
        data = self.get_mock_sign_up_data()
        self.assert_sign_up_successful(data)
