import time

from flask import url_for
from itsdangerous import TimedJSONWebSignatureSerializer, URLSafeSerializer

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
        return {'email': email() if callable(email) else email}

    def get_verify_token(self, auth_id):
        return URLSafeSerializer(self.app.secret_key).dumps(auth_id)

    def get_mock_login_data(self,
                            email=fake.email,
                            password=fake.password):
        return {
            'email': email() if callable(email) else email,
            'password': password() if callable(password) else password,
        }

    def get_mock_reset_password_request_data(self, email=fake.email):
        return {'email': email() if callable(email) else email}

    def get_reset_password_token(self, auth_id, expires_in=3600):
        return TimedJSONWebSignatureSerializer(self.app.secret_key, expires_in).dumps(auth_id).decode('utf-8')

    def get_mock_reset_password_data(self,
                                     password=fake.password,
                                     confirmation=fake.password):
        return {
            'password': password() if callable(password) else password,
            'confirmation': confirmation() if callable(confirmation) else confirmation,
        }

    #
    # sign_up_GET tests.
    #

    def test_sign_up_GET(self):
        response = self.client.get(url_for('auth.sign_up_GET'))
        assert response.status_code == 200

    #
    # sign_up_POST tests.
    #

    def assert_sign_up_POST_successful(self, data):
        response = self.client.post(url_for('auth.sign_up_POST'), data=data)
        user = User.objects(email=data['email']).first()
        assert response.status_code == 302
        assert not user.is_active
        assert user.initials
        assert user.name == data['name']
        assert user.verify_password(data['password'])

    def assert_sign_up_POST_unsuccessful(self, data):
        response = self.client.post(url_for('auth.sign_up_POST'), data=data)
        user = User.objects(email=data['email']).first()
        assert response.status_code == 400
        assert user is None or user == self.user

    def test_sign_up_POST_no_name(self):
        name = None
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_name_length_equal_to_minimum(self):
        name = fake.pystr(min_chars=1, max_chars=1)
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_POST_successful(data)

    def test_sign_up_POST_name_length_equal_to_maximum(self):
        name = fake.pystr(min_chars=50, max_chars=50)
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_POST_successful(data)

    def test_sign_up_POST_name_length_greater_than_maximum(self):
        name = fake.pystr(min_chars=51, max_chars=51)
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_no_email(self):
        email = None
        data = self.get_mock_sign_up_data(email=email)
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_invalid_email(self):
        email = fake.sentence()
        data = self.get_mock_sign_up_data(email=email)
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_no_password(self):
        password = None
        data = self.get_mock_sign_up_data(password=password)
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_password_length_less_than_minimum(self):
        password = fake.pystr(min_chars=7, max_chars=7)
        data = self.get_mock_sign_up_data(password=password)
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_password_length_equal_to_minimum(self):
        password = fake.pystr(min_chars=8, max_chars=8)
        data = self.get_mock_sign_up_data(password=password)
        self.assert_sign_up_POST_successful(data)

    def test_sign_up_POST_account_already_exists(self):
        email = self.user.email
        data = self.get_mock_sign_up_data(email=email)
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_success(self):
        data = self.get_mock_sign_up_data()
        self.assert_sign_up_POST_successful(data)

    #
    # verify_resend_GET tests.
    #

    def test_verify_resend_GET(self):
        response = self.client.get(url_for('auth.verify_resend_GET'))
        assert response.status_code == 200

    #
    # verify_resend_POST tests.
    #

    def assert_verify_resend_POST_successful(self, data):
        response = self.client.post(url_for('auth.verify_resend_POST'), data=data)
        assert response.status_code == 200

    def assert_verify_resend_POST_unsuccessful(self, data):
        response = self.client.post(url_for('auth.verify_resend_POST'), data=data)
        assert response.status_code == 400

    def test_verify_resend_POST_no_email(self):
        email = None
        data = self.get_mock_verify_resend_data(email=email)
        self.assert_verify_resend_POST_unsuccessful(data)

    def test_verify_resend_POST_invalid_email(self):
        email = fake.sentence()
        data = self.get_mock_verify_resend_data(email=email)
        self.assert_verify_resend_POST_unsuccessful(data)

    def test_verify_resend_POST_account_does_not_exist(self):
        user = self.create_user()
        user.delete()
        data = self.get_mock_verify_resend_data(email=user.email)
        self.assert_verify_resend_POST_unsuccessful(data)

    def test_verify_resend_POST_account_already_verified(self):
        data = self.get_mock_verify_resend_data(email=self.user.email)
        self.assert_verify_resend_POST_unsuccessful(data)

    def test_verify_resend_POST_success(self):
        user = self.create_user(active=False)
        data = self.get_mock_verify_resend_data(email=user.email)
        self.assert_verify_resend_POST_successful(data)

    #
    # /auth/verify/<token> tests.
    #

    def assert_verify_successful(self, token, email):
        response = self.client.get('/auth/verify/{}'.format(token))
        user = User.objects(email=email).first()
        assert response.status_code == 302
        assert user.is_active
        assert user.last_updated

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

    def assert_login_unsuccessful(self, data, redirect_target=None):
        path = '/auth/login?next={}'.format(redirect_target) if redirect_target else '/auth/login'
        response = self.client.post(path, data=data)
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

    def test_login_bad_redirect_target(self):
        data = self.get_mock_login_data(email=self.user.email, password=self.password)
        self.assert_login_unsuccessful(data, 'https://github.com/')

    def test_login_success(self):
        data = self.get_mock_login_data(email=self.user.email, password=self.password)
        self.assert_login_successful(data)

    #
    # /auth/logout tests.
    #

    def test_logout_success(self):
        response = self.client.get('/auth/logout')
        assert response.status_code == 200

    #
    # /auth/reset-password tests.
    #

    def assert_reset_password_request_successful(self, data):
        self.logout()
        response = self.client.post('/auth/reset-password', data=data)
        assert response.status_code == 200

    def assert_reset_password_request_unsuccessful(self, data):
        self.logout()
        response = self.client.post('/auth/reset-password', data=data)
        assert response.status_code == 400

    def test_reset_password_request_GET(self):
        response = self.client.get('/auth/reset-password')
        assert response.status_code == 200

    def test_reset_password_request_no_email(self):
        email = None
        data = self.get_mock_reset_password_request_data(email=email)
        self.assert_reset_password_request_unsuccessful(data)

    def test_reset_password_request_invalid_email(self):
        email = fake.sentence()
        data = self.get_mock_reset_password_request_data(email=email)
        self.assert_reset_password_request_unsuccessful(data)

    def test_reset_password_request_account_does_not_exist(self):
        user = self.create_user(active=False)
        user.delete()
        data = self.get_mock_reset_password_request_data(email=user.email)
        self.assert_reset_password_request_unsuccessful(data)

    def test_reset_password_request_success(self):
        user = self.create_user(active=False)
        data = self.get_mock_reset_password_request_data(email=user.email)
        self.assert_reset_password_request_successful(data)

    #
    # /auth/reset-password/<token> tests.
    #

    def assert_reset_password_successful(self, user_id, auth_id, data):
        token = self.get_reset_password_token(auth_id=str(auth_id))
        response = self.client.post('/auth/reset-password/{}'.format(token), data=data)
        user = User.objects(id=user_id).first()
        assert response.status_code == 302
        assert user.auth_id != auth_id
        assert user.last_updated
        assert user.verify_password(data['password'])

    def assert_reset_password_unsuccessful(self, auth_id, data):
        token = self.get_reset_password_token(auth_id=str(auth_id))
        response = self.client.post('/auth/reset-password/{}'.format(token), data=data)
        user = User.objects(auth_id=auth_id).first()
        assert response.status_code == 400
        assert user.last_updated is None
        assert not user.verify_password(data['password'])

    def assert_reset_password_token_error(self, token):
        response = self.client.get('/auth/reset-password/{}'.format(token))
        assert response.status_code == 404

    def test_reset_password_invalid_token(self):
        token = self.get_reset_password_token('invalid token')
        self.assert_reset_password_token_error(token)

    def test_reset_password_expired_token(self):
        token = self.get_reset_password_token(auth_id=str(self.user.auth_id), expires_in=1)
        time.sleep(2)
        self.assert_reset_password_token_error(token)

    def test_reset_password_account_does_not_exist(self):
        user = self.create_user(active=False)
        user.delete()
        token = self.get_reset_password_token(str(user.auth_id))
        self.assert_reset_password_token_error(token)

    def test_reset_password_GET(self):
        token = self.get_reset_password_token(auth_id=str(self.user.auth_id))
        response = self.client.get('/auth/reset-password/{}'.format(token))
        assert response.status_code == 200

    def test_reset_password_no_password(self):
        password = None
        data = self.get_mock_reset_password_data(password=password, confirmation=password)
        self.assert_reset_password_unsuccessful(self.user.auth_id, data)

    def test_reset_password_less_than_minimum(self):
        password = fake.pystr(min_chars=7, max_chars=7)
        data = self.get_mock_reset_password_data(password=password, confirmation=password)
        self.assert_reset_password_unsuccessful(self.user.auth_id, data)

    def test_reset_password_length_equal_to_minimum(self):
        password = fake.pystr(min_chars=8, max_chars=8)
        data = self.get_mock_reset_password_data(password=password, confirmation=password)
        self.assert_reset_password_successful(self.user.id, self.user.auth_id, data)

    def test_reset_password_and_confirmation_dont_match(self):
        password = 'password'
        confirmation = 'confirmation'
        data = self.get_mock_reset_password_data(password=password, confirmation=confirmation)
        self.assert_reset_password_unsuccessful(self.user.auth_id, data)

    def test_reset_password_success(self):
        password = fake.password()
        data = self.get_mock_reset_password_data(password=password, confirmation=password)
        self.assert_reset_password_successful(self.user.id, self.user.auth_id, data)
