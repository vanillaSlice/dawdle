import time
from unittest import mock

from flask import url_for
from itsdangerous import TimedJSONWebSignatureSerializer, URLSafeSerializer

from dawdle.models.user import User
from tests.test_base import TestBase

class TestAuth(TestBase):

    #
    # Utils
    #

    def get_mock_sign_up_data(self, **kwargs):
        return {
            'email': kwargs.get('email', self.fake.email()),
            'name': kwargs.get('name', self.fake.name()),
            'password': kwargs.get('password', self.fake.password()),
        }

    def get_mock_verify_resend_data(self, **kwargs):
        return {'email': kwargs.get('email', self.fake.email())}

    def get_verify_token(self, auth_id):
        return URLSafeSerializer(self.app.secret_key).dumps(auth_id)

    def get_mock_login_data(self, **kwargs):
        return {
            'email': kwargs.get('email', self.fake.email()),
            'password': kwargs.get('password', self.fake.password()),
        }

    def get_mock_reset_password_request_data(self, **kwargs):
        return {'email': kwargs.get('email', self.fake.email())}

    def get_reset_password_token(self, auth_id, expires_in=3600):
        return TimedJSONWebSignatureSerializer(self.app.secret_key, expires_in).dumps(auth_id).decode('utf-8')

    def get_mock_reset_password_data(self, **kwargs):
        return {
            'password': kwargs.get('password', self.fake.password()),
            'confirmation': kwargs.get('confirmation', self.fake.password()),
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
        user = User.objects(email=data.get('email')).first()
        assert response.status_code == 400
        assert user is None or user == self.user

    def test_sign_up_POST_no_name(self):
        data = self.get_mock_sign_up_data()
        del data['name']
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_name_length_equal_to_minimum(self):
        name = self.fake.pystr(min_chars=1, max_chars=1)
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_POST_successful(data)

    def test_sign_up_POST_name_length_equal_to_maximum(self):
        name = self.fake.pystr(min_chars=50, max_chars=50)
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_POST_successful(data)

    def test_sign_up_POST_name_length_greater_than_maximum(self):
        name = self.fake.pystr(min_chars=51, max_chars=51)
        data = self.get_mock_sign_up_data(name=name)
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_no_email(self):
        data = self.get_mock_sign_up_data()
        del data['email']
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_invalid_email(self):
        email = self.fake.sentence()
        data = self.get_mock_sign_up_data(email=email)
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_no_password(self):
        data = self.get_mock_sign_up_data()
        del data['password']
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_password_length_less_than_minimum(self):
        password = self.fake.pystr(min_chars=7, max_chars=7)
        data = self.get_mock_sign_up_data(password=password)
        self.assert_sign_up_POST_unsuccessful(data)

    def test_sign_up_POST_password_length_equal_to_minimum(self):
        password = self.fake.pystr(min_chars=8, max_chars=8)
        data = self.get_mock_sign_up_data(password=password)
        self.assert_sign_up_POST_successful(data)

    def test_sign_up_POST_account_already_exists(self):
        email = self.user.email
        data = self.get_mock_sign_up_data(email=email)
        self.assert_sign_up_POST_unsuccessful(data)

    @mock.patch('dawdle.utils.mail')
    def test_sign_up_POST_error_sending_email(self, mail_mock):
        mail_mock.send.side_effect = RuntimeError('some error')
        data = self.get_mock_sign_up_data()
        self.assert_sign_up_POST_successful(data)

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

    def assert_verify_resend_POST_response(self, data, status_code, email=None):
        response = self.client.post(url_for('auth.verify_resend_POST', email=email), data=data)
        assert response.status_code == status_code

    def test_verify_resend_POST_no_email(self):
        data = self.get_mock_verify_resend_data()
        del data['email']
        self.assert_verify_resend_POST_response(data, 400)

    def test_verify_resend_POST_email_in_request(self):
        user = self.create_user(active=False)
        data = self.get_mock_verify_resend_data()
        del data['email']
        self.assert_verify_resend_POST_response(data, 200, email=user.email)

    def test_verify_resend_POST_invalid_email(self):
        email = self.fake.sentence()
        data = self.get_mock_verify_resend_data(email=email)
        self.assert_verify_resend_POST_response(data, 400)

    def test_verify_resend_POST_account_does_not_exist(self):
        user = self.create_user()
        user.delete()
        data = self.get_mock_verify_resend_data(email=user.email)
        self.assert_verify_resend_POST_response(data, 400)

    def test_verify_resend_POST_account_already_verified(self):
        data = self.get_mock_verify_resend_data(email=self.user.email)
        self.assert_verify_resend_POST_response(data, 400)

    @mock.patch('dawdle.utils.mail')
    def test_verify_resend_POST_error_sending_email(self, mail_mock):
        mail_mock.send.side_effect = RuntimeError('some error')
        user = self.create_user(active=False)
        data = self.get_mock_verify_resend_data(email=user.email)
        self.assert_verify_resend_POST_response(data, 500)

    def test_verify_resend_POST_success(self):
        user = self.create_user(active=False)
        data = self.get_mock_verify_resend_data(email=user.email)
        self.assert_verify_resend_POST_response(data, 200)

    #
    # verify_GET tests.
    #

    def assert_verify_GET_successful(self, token, email):
        response = self.client.get(url_for('auth.verify_GET', token=token))
        user = User.objects(email=email).first()
        assert response.status_code == 302
        assert user.is_active
        assert user.last_updated

    def assert_verify_GET_unsuccessful(self, token, email):
        response = self.client.get(url_for('auth.verify_GET', token=token))
        user = User.objects(email=email).first()
        assert response.status_code == 404
        assert user is None or not user.is_active

    def test_verify_GET_invalid_token(self):
        user = self.create_user(active=False)
        token = 'invalid token'
        self.assert_verify_GET_unsuccessful(token, user.email)

    def test_verify_GET_invalid_auth_id(self):
        user = self.create_user(active=False)
        token = self.get_verify_token('invalid auth id')
        self.assert_verify_GET_unsuccessful(token, user.email)

    def test_verify_GET_account_does_not_exist(self):
        user = self.create_user(active=False)
        user.delete()
        token = self.get_verify_token(str(user.auth_id))
        self.assert_verify_GET_unsuccessful(token, user.email)

    def test_verify_GET_bad_redirect_target(self):
        user = self.create_user(active=False)
        token = self.get_verify_token(str(user.auth_id))
        response = self.client.get(url_for('auth.verify_GET', token=token, next='https://github.com/'))
        assert response.status_code == 400

    def test_verify_GET_success(self):
        user = self.create_user(active=False)
        token = self.get_verify_token(str(user.auth_id))
        self.assert_verify_GET_successful(token, user.email)

    #
    # login_GET tests.
    #

    def test_login_GET(self):
        response = self.client.get(url_for('auth.login_GET'))
        assert response.status_code == 200

    #
    # login_POST tests.
    #

    def assert_login_POST_successful(self, data):
        response = self.client.post(url_for('auth.login_POST'), data=data)
        assert response.status_code == 302

    def assert_login_POST_unsuccessful(self, data, redirect_target=None):
        path = url_for('auth.login_POST', next=redirect_target)
        response = self.client.post(path, data=data)
        assert response.status_code == 400

    def test_login_POST_no_email(self):
        data = self.get_mock_login_data()
        del data['email']
        self.assert_login_POST_unsuccessful(data)

    def test_login_POST_invalid_email(self):
        email = self.fake.sentence()
        data = self.get_mock_login_data(email=email)
        self.assert_login_POST_unsuccessful(data)

    def test_login_POST_no_password(self):
        data = self.get_mock_login_data()
        del data['password']
        self.assert_login_POST_unsuccessful(data)

    def test_login_POST_account_does_not_exist(self):
        user = self.create_user(password='user password', active=True)
        user.delete()
        data = self.get_mock_login_data(email=user.email, password=user.password)
        self.assert_login_POST_unsuccessful(data)

    def test_login_POST_incorrect_password(self):
        password = 'incorrect password'
        data = self.get_mock_sign_up_data(email=self.user.email, password=password)
        self.assert_login_POST_unsuccessful(data)

    def test_login_POST_inactive_account(self):
        password = 'user password'
        user = self.create_user(password=password, active=False)
        data = self.get_mock_login_data(email=user.email, password=password)
        self.assert_login_POST_unsuccessful(data)

    def test_login_POST_bad_redirect_target(self):
        data = self.get_mock_login_data(email=self.user.email, password=self.password)
        self.assert_login_POST_unsuccessful(data, 'https://github.com/')

    def test_login_POST_success(self):
        data = self.get_mock_login_data(email=self.user.email, password=self.password)
        self.assert_login_POST_successful(data)

    #
    # logout_GET tests.
    #

    def test_logout_GET_success(self):
        response = self.client.get(url_for('auth.logout_GET'))
        assert response.status_code == 302

    #
    # reset_password_request_GET tests.
    #

    def test_reset_password_request_GET(self):
        response = self.client.get(url_for('auth.reset_password_request_GET'))
        assert response.status_code == 200

    #
    # reset_password_request_POST tests.
    #

    def assert_reset_password_request_POST_response(self, data, status_code):
        self.logout()
        response = self.client.post(url_for('auth.reset_password_request_POST'), data=data)
        assert response.status_code == status_code

    def test_reset_password_request_POST_no_email_not_authenticated(self):
        self.logout()
        data = self.get_mock_reset_password_request_data()
        del data['email']
        self.assert_reset_password_request_POST_response(data, 400)

    def test_reset_password_request_POST_invalid_email(self):
        email = self.fake.sentence()
        data = self.get_mock_reset_password_request_data(email=email)
        self.assert_reset_password_request_POST_response(data, 400)

    def test_reset_password_request_POST_account_does_not_exist(self):
        user = self.create_user(active=False)
        user.delete()
        data = self.get_mock_reset_password_request_data(email=user.email)
        self.assert_reset_password_request_POST_response(data, 400)

    @mock.patch('dawdle.blueprints.auth.mail')
    def test_reset_password_request_POST_error_sending_email(self, mail_mock):
        mail_mock.send.side_effect = RuntimeError('some error')
        user = self.create_user(active=False)
        data = self.get_mock_reset_password_request_data(email=user.email)
        self.assert_reset_password_request_POST_response(data, 500)

    def test_reset_password_request_POST_success(self):
        user = self.create_user(active=False)
        data = self.get_mock_reset_password_request_data(email=user.email)
        self.assert_reset_password_request_POST_response(data, 200)

    #
    # reset_password_GET tests.
    #

    def assert_reset_password_GET_response(self, token, status_code):
        response = self.client.get(url_for('auth.reset_password_GET', token=token))
        assert response.status_code == status_code

    def test_reset_password_GET(self):
        token = self.get_reset_password_token(auth_id=str(self.user.auth_id))
        self.assert_reset_password_GET_response(token, 200)

    def test_reset_password_GET_invalid_token(self):
        token = 'invalid token'
        self.assert_reset_password_GET_response(token, 404)

    def test_reset_password_GET_invalid_auth_id(self):
        token = self.get_reset_password_token('invalid auth id')
        self.assert_reset_password_GET_response(token, 404)

    def test_reset_password_GET_expired_token(self):
        token = self.get_reset_password_token(auth_id=str(self.user.auth_id), expires_in=1)
        time.sleep(2)
        self.assert_reset_password_GET_response(token, 404)

    def test_reset_password_GET_account_does_not_exist(self):
        user = self.create_user(active=False)
        user.delete()
        token = self.get_reset_password_token(str(user.auth_id))
        self.assert_reset_password_GET_response(token, 404)

    #
    # reset_password_POST tests.
    #

    def assert_reset_password_POST_successful(self, user_id, auth_id, data):
        token = self.get_reset_password_token(auth_id=str(auth_id))
        response = self.client.post(url_for('auth.reset_password_POST', token=token), data=data)
        user = User.objects(id=user_id).first()
        assert response.status_code == 302
        assert user.auth_id != auth_id
        assert user.last_updated
        assert user.verify_password(data['password'])

    def assert_reset_password_POST_unsuccessful(self, auth_id, data):
        token = self.get_reset_password_token(auth_id=str(auth_id))
        response = self.client.post(url_for('auth.reset_password_POST', token=token), data=data)
        user = User.objects(auth_id=auth_id).first()
        assert response.status_code == 400
        assert user.last_updated is None
        assert not user.verify_password(data.get('password'))

    def test_reset_password_POST_no_password(self):
        user = self.create_user(active=True)
        data = self.get_mock_reset_password_data()
        del data['password']
        self.assert_reset_password_POST_unsuccessful(user.auth_id, data)

    def test_reset_password_POST_password_length_less_than_minimum(self):
        user = self.create_user(active=True)
        password = self.fake.pystr(min_chars=7, max_chars=7)
        data = self.get_mock_reset_password_data(password=password, confirmation=password)
        self.assert_reset_password_POST_unsuccessful(user.auth_id, data)

    def test_reset_password_POST_password_length_equal_to_minimum(self):
        user = self.create_user(active=True)
        password = self.fake.pystr(min_chars=8, max_chars=8)
        data = self.get_mock_reset_password_data(password=password, confirmation=password)
        self.assert_reset_password_POST_successful(user.id, user.auth_id, data)

    def test_reset_password_POST_password_and_confirmation_dont_match(self):
        user = self.create_user(active=True)
        password = 'password'
        confirmation = 'confirmation'
        data = self.get_mock_reset_password_data(password=password, confirmation=confirmation)
        self.assert_reset_password_POST_unsuccessful(user.auth_id, data)

    def test_reset_password_POST_success(self):
        user = self.create_user(active=True)
        password = self.fake.password()
        data = self.get_mock_reset_password_data(password=password, confirmation=password)
        self.assert_reset_password_POST_successful(user.id, user.auth_id, data)
