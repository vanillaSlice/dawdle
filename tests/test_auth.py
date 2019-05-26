from itsdangerous import URLSafeSerializer

from dawdle.models.user import User
from tests.test_base import fake, TestBase

class TestAuth(TestBase):

    #
    # Utils
    #

    def get_mock_sign_up_data(self,
                              email=fake.email,
                              name=fake.name,
                              password=fake.password):
        return {
            'email': email() if callable(email) else email,
            'name': name() if callable(name) else name,
            'password': password() if callable(password) else password,
        }

    def get_mock_verify_resend_data(self, email=fake.email):
        return {
            'email': email() if callable(email) else email,
        }

    def get_verify_token(self, auth_id):
        return URLSafeSerializer(self.app.secret_key).dumps(auth_id)

    def get_mock_login_data(self,
                            email=fake.email,
                            password=fake.password):
        return {
            'email': email() if callable(email) else email,
            'password': password() if callable(password) else password,
        }

    #
    # /auth/sign-up tests.
    #

    def assert_sign_up_successful(self, data):
        response = self.client.post('/auth/sign-up', data=data)
        user = User.objects(email=data['email']).first()
        assert response.status_code == 302
        assert not user.is_active
        assert user.name == data['name']
        assert user.verify_password(data['password'])

    def assert_sign_up_unsuccessful(self, data):
        response = self.client.post('/auth/sign-up', data=data)
        user = User.objects(email=data['email']).first()
        assert response.status_code == 400
        assert not user or user == self.user

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

    #
    # /auth/verify/resend tests.
    #

    def assert_verify_resend_successful(self, data):
        response = self.client.post('/auth/verify/resend', data=data)
        assert response.status_code == 302

    def assert_verify_resend_unsuccessful(self, data):
        response = self.client.post('/auth/verify/resend', data=data)
        assert response.status_code == 400

    def test_verify_resend_GET(self):
        response = self.client.get('/auth/verify/resend')
        assert response.status_code == 200

    def test_verify_resend_no_email(self):
        email = None
        data = self.get_mock_verify_resend_data(email=email)
        self.assert_verify_resend_unsuccessful(data)

    def test_verify_resend_invalid_email(self):
        email = fake.sentence()
        data = self.get_mock_verify_resend_data(email=email)
        self.assert_verify_resend_unsuccessful(data)

    def test_verify_resend_account_does_not_exist(self):
        user = self.create_user()
        user.delete()
        data = self.get_mock_verify_resend_data(email=user.email)
        self.assert_verify_resend_unsuccessful(data)

    def test_verify_resend_account_already_verified(self):
        data = self.get_mock_verify_resend_data(email=self.user.email)
        self.assert_verify_resend_unsuccessful(data)

    def test_verify_resend_success(self):
        user = self.create_user(active=False)
        data = self.get_mock_verify_resend_data(email=user.email)
        self.assert_verify_resend_successful(data)

    #
    # /auth/verify/<token> tests.
    #

    def assert_verify_successful(self, token, email):
        response = self.client.get('/auth/verify/{}'.format(token))
        user = User.objects(email=email).first()
        assert response.status_code == 302
        assert user.is_active

    def assert_verify_unsuccessful(self, token, email):
        response = self.client.get('/auth/verify/{}'.format(token))
        user = User.objects(email=email).first()
        assert response.status_code == 404
        assert user is None or not user.is_active

    def test_verify_invalid_token(self):
        user = self.create_user(active=False)
        token = self.get_verify_token('invalid token')
        self.assert_verify_unsuccessful(token, user.email)

    def test_verify_account_does_not_exist(self):
        user = self.create_user(active=False)
        user.delete()
        token = self.get_verify_token(str(user.auth_id))
        self.assert_verify_unsuccessful(token, user.email)

    def test_verify_account_already_active(self):
        token = self.get_verify_token(str(self.user.auth_id))
        self.assert_verify_successful(token, self.user.email)

    def test_verify_success(self):
        user = self.create_user(active=False)
        token = self.get_verify_token(str(user.auth_id))
        self.assert_verify_successful(token, user.email)

    #
    # /auth/login tests.
    #

    def assert_login_successful(self, data):
        response = self.client.post('/auth/login', data=data)
        assert response.status_code == 302

    def assert_login_unsuccessful(self, data):
        response = self.client.post('/auth/login', data=data)
        assert response.status_code == 400

    def test_login_GET(self):
        response = self.client.get('/auth/login')
        assert response.status_code == 200

    def test_login_no_email(self):
        email = None
        data = self.get_mock_login_data(email=email)
        self.assert_login_unsuccessful(data)

    def test_login_invalid_email(self):
        email = fake.sentence()
        data = self.get_mock_login_data(email=email)
        self.assert_login_unsuccessful(data)

    def test_login_no_password(self):
        password = None
        data = self.get_mock_login_data(password=password)
        self.assert_login_unsuccessful(data)

    def test_login_account_does_not_exist(self):
        user = self.create_user(password='user password', active=True)
        user.delete()
        data = self.get_mock_login_data(email=user.email, password=user.password)
        self.assert_login_unsuccessful(data)

    def test_login_incorrect_password(self):
        password = 'incorrect password'
        data = self.get_mock_sign_up_data(email=self.user.email, password=password)
        self.assert_login_unsuccessful(data)

    def test_login_inactive_account(self):
        password = 'user password'
        user = self.create_user(password=password, active=False)
        data = self.get_mock_login_data(email=user.email, password=password)
        self.assert_login_unsuccessful(data)

    def test_login_success(self):
        data = self.get_mock_login_data(email=self.user.email, password=self.password)
        self.assert_login_successful(data)

    #
    # /auth/logout tests.
    #

    def test_logout_success(self):
        response = self.client.get('/auth/logout')
        assert response.status_code == 200
