from flask import url_for

from dawdle.models.user import User
from tests.test_base import TestBase

class TestUser(TestBase):

    #
    # Utils
    #

    def get_mock_update_password_data(self, **kwargs):
        return {
            'current_password': kwargs.get('current_password', self.fake.password()),
            'new_password': kwargs.get('new_password', self.fake.password()),
            'confirmation': kwargs.get('confirmation', self.fake.password()),
        }

    def get_mock_delete_account_data(self, **kwargs):
        return {'password': kwargs.get('password', self.fake.password())}

    #
    # boards_GET tests.
    #

    def assert_boards_GET_response(self, status_code):
        response = self.client.get(url_for('user.boards_GET'))
        assert response.status_code == status_code

    def test_boards_GET_not_authenticated(self):
        self.logout()
        self.assert_boards_GET_response(302)

    def test_boards_GET_authenticated(self):
        self.assert_boards_GET_response(200)

    #
    # settings_GET tests.
    #

    def assert_settings_GET_response(self, status_code):
        response = self.client.get(url_for('user.settings_GET'))
        assert response.status_code == status_code

    def test_settings_GET_not_authenticated(self):
        self.logout()
        self.assert_settings_GET_response(302)

    def test_settings_GET_authenticated(self):
        self.assert_settings_GET_response(302)

    #
    # settings_update_password_GET tests.
    #

    def assert_settings_update_password_GET_response(self, status_code):
        response = self.client.get(url_for('user.settings_update_password_GET'))
        assert response.status_code == status_code

    def test_settings_update_password_GET_not_authenticated(self):
        self.logout()
        self.assert_settings_update_password_GET_response(302)

    def test_settings_update_password_GET_authenticated(self):
        self.assert_settings_update_password_GET_response(200)

    #
    # settings_update_password_POST tests.
    #

    def assert_settings_update_password_POST_successful(self, user_id, auth_id, data):
        response = self.client.post(url_for('user.settings_update_password_POST'), data=data)
        user = User.objects(id=user_id).first()
        assert response.status_code == 302
        assert user.auth_id != auth_id
        assert user.last_updated
        assert user.verify_password(data['new_password'])

    def assert_settings_update_password_POST_unsuccessful(self, auth_id, data):
        response = self.client.post(url_for('user.settings_update_password_POST'), data=data)
        user = User.objects(auth_id=auth_id).first()
        assert response.status_code == 400
        assert user.last_updated is None

    def test_settings_update_password_POST_not_authenticated(self):
        self.logout()
        response = self.client.post(url_for('user.settings_update_password_POST'))
        assert response.status_code == 302

    def test_settings_update_password_POST_incorrect_current_password(self):
        user = self.create_user(active=True, password='password')
        self.login(email=user.email, password='password')
        current_password = 'wrong'
        new_password = self.fake.pystr(min_chars=8, max_chars=8)
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_unsuccessful(user.auth_id, data)

    def test_settings_update_password_POST_new_password_length_less_than_minimum(self):
        user = self.create_user(active=True, password='password')
        self.login(email=user.email, password='password')
        current_password = 'password'
        new_password = self.fake.pystr(min_chars=7, max_chars=7)
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_unsuccessful(user.auth_id, data)

    def test_settings_update_password_POST_new_password_length_equal_to_minimum(self):
        user = self.create_user(active=True, password='password')
        self.login(email=user.email, password='password')
        current_password = 'password'
        new_password = self.fake.pystr(min_chars=8, max_chars=8)
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_successful(user.id, user.auth_id, data)

    def test_settings_update_password_POST_new_password_and_confirmation_dont_match(self):
        user = self.create_user(active=True, password='password')
        self.login(email=user.email, password='password')
        current_password = 'password'
        new_password = self.fake.pystr(min_chars=8, max_chars=8)
        confirmation = 'wrong'
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_unsuccessful(user.auth_id, data)

    def test_settings_update_password_POST_success(self):
        user = self.create_user(active=True, password='password')
        self.login(email=user.email, password='password')
        current_password = 'password'
        new_password = self.fake.pystr(min_chars=8, max_chars=8)
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_successful(user.id, user.auth_id, data)

    #
    # settings_delete_account_GET tests.
    #

    def test_settings_delete_account_GET_not_authenticated(self):
        self.logout()
        response = self.client.get(url_for('user.settings_delete_account_GET'))
        assert response.status_code == 302

    def test_settings_delete_account_GET_authenticated(self):
        response = self.client.get(url_for('user.settings_delete_account_GET'))
        assert response.status_code == 200

    #
    # settings_delete_account_POST tests.
    #

    def assert_settings_delete_account_POST_response(self, data, status_code):
        response = self.client.post(url_for('user.settings_delete_account_POST'), data=data)
        assert response.status_code == status_code

    def test_settings_delete_account_POST_not_authenticated(self):
        self.logout()
        data = self.get_mock_delete_account_data()
        self.assert_settings_delete_account_POST_response(data, 302)

    def test_settings_delete_account_POST_incorrect_password(self):
        password = 'password'
        user = self.create_user(active=True, password=password)
        self.login(email=user.email, password=password)
        data = self.get_mock_delete_account_data(password='wrong')
        self.assert_settings_delete_account_POST_response(data, 400)

    def test_settings_delete_account_POST_success(self):
        password = 'password'
        user = self.create_user(active=True, password=password)
        self.login(email=user.email, password=password)
        data = self.get_mock_delete_account_data(password=password)
        self.assert_settings_delete_account_POST_response(data, 302)
