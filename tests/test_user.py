from unittest import mock

from flask import url_for

from dawdle.models.user import User
from tests.test_base import TestBase

class TestUser(TestBase):

    #
    # Utils
    #

    def get_mock_account_details_data(self, **kwargs):
        return {
            'name': kwargs.get('name', self.fake.name()),
            'initials': kwargs.get('initials', self.fake.pystr(min_chars=1, max_chars=4)),
        }

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

    def test_boards_GET(self):
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

    def test_settings_GET(self):
        self.assert_settings_GET_response(302)

    #
    # settings_account_details_GET tests.
    #

    def assert_settings_account_details_GET_response(self, status_code):
        response = self.client.get(url_for('user.settings_account_details_GET'))
        assert response.status_code == status_code

    def test_settings_account_details_GET_not_authenticated(self):
        self.logout()
        self.assert_settings_account_details_GET_response(302)

    def test_settings_account_details_GET(self):
        self.assert_settings_account_details_GET_response(200)

    #
    # settings_account_details_POST tests.
    #

    def assert_settings_account_details_POST_successful(self, data):
        user, password = self.with_new_user()
        response = self.client.post(url_for('user.settings_account_details_POST'), data=data)
        user = User.objects(id=user.id).first()
        assert response.status_code == 302
        assert user.initials == data['initials']
        assert user.last_updated
        assert user.name == data['name']

    def assert_settings_account_details_POST_unsuccessful(self, data):
        user, password = self.with_new_user()
        response = self.client.post(url_for('user.settings_account_details_POST'), data=data)
        user = User.objects(id=user.id).first()
        assert response.status_code == 400
        assert user.last_updated is None

    def test_settings_account_details_POST_name_length_equal_to_minimum(self):
        name = self.fake.pystr(min_chars=1, max_chars=1)
        data = self.get_mock_account_details_data(name=name)
        self.assert_settings_account_details_POST_successful(data)

    def test_settings_account_details_POST_name_length_equal_to_maximum(self):
        name = self.fake.pystr(min_chars=50, max_chars=50)
        data = self.get_mock_account_details_data(name=name)
        self.assert_settings_account_details_POST_successful(data)

    def test_settings_account_details_POST_name_length_greater_than_maximum(self):
        name = self.fake.pystr(min_chars=51, max_chars=51)
        data = self.get_mock_account_details_data(name=name)
        self.assert_settings_account_details_POST_unsuccessful(data)

    def test_settings_account_details_POST_initials_length_equal_to_minimum(self):
        initials = self.fake.pystr(min_chars=1, max_chars=1)
        data = self.get_mock_account_details_data(initials=initials)
        self.assert_settings_account_details_POST_successful(data)

    def test_settings_account_details_POST_initials_length_equal_to_maximum(self):
        initials = self.fake.pystr(min_chars=4, max_chars=4)
        data = self.get_mock_account_details_data(initials=initials)
        self.assert_settings_account_details_POST_successful(data)

    def test_settings_account_details_POST_initials_length_greater_than_maximum(self):
        initials = self.fake.pystr(min_chars=5, max_chars=5)
        data = self.get_mock_account_details_data(initials=initials)
        self.assert_settings_account_details_POST_unsuccessful(data)

    def test_settings_account_details_POST_success(self):
        data = self.get_mock_account_details_data()
        self.assert_settings_account_details_POST_successful(data)

    #
    # settings_update_email_GET tests.
    #

    def assert_settings_update_email_GET_response(self, status_code):
        response = self.client.get(url_for('user.settings_update_email_GET'))
        assert response.status_code == status_code

    def test_settings_update_email_GET_not_authenticated(self):
        self.logout()
        self.assert_settings_update_email_GET_response(302)

    def test_settings_update_email_GET(self):
        self.assert_settings_update_email_GET_response(200)

    #
    # settings_update_password_GET tests.
    #

    def assert_settings_update_password_GET_response(self, status_code):
        response = self.client.get(url_for('user.settings_update_password_GET'))
        assert response.status_code == status_code

    def test_settings_update_password_GET_not_authenticated(self):
        self.logout()
        self.assert_settings_update_password_GET_response(302)

    def test_settings_update_password_GET(self):
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
        user, password = self.with_new_user()
        current_password = 'wrong'
        new_password = self.fake.password()
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_unsuccessful(user.auth_id, data)

    def test_settings_update_password_POST_new_password_length_less_than_minimum(self):
        user, password = self.with_new_user()
        current_password = password
        new_password = self.fake.pystr(min_chars=7, max_chars=7)
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_unsuccessful(user.auth_id, data)

    def test_settings_update_password_POST_new_password_length_equal_to_minimum(self):
        user, password = self.with_new_user()
        current_password = password
        new_password = self.fake.pystr(min_chars=8, max_chars=8)
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_successful(user.id, user.auth_id, data)

    def test_settings_update_password_POST_new_password_and_confirmation_dont_match(self):
        user, password = self.with_new_user()
        current_password = password
        new_password = self.fake.password()
        confirmation = 'wrong'
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_unsuccessful(user.auth_id, data)

    def test_settings_update_password_POST_success(self):
        user, password = self.with_new_user()
        current_password = password
        new_password = self.fake.password()
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_successful(user.id, user.auth_id, data)

    #
    # settings_delete_account_GET tests.
    #

    def assert_settings_delete_account_GET_response(self, status_code):
        response = self.client.get(url_for('user.settings_delete_account_GET'))
        assert response.status_code == status_code

    def test_settings_delete_account_GET_not_authenticated(self):
        self.logout()
        self.assert_settings_delete_account_GET_response(302)

    def test_settings_delete_account_GET(self):
        self.assert_settings_delete_account_GET_response(200)

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

    def test_settings_delete_account_POST_no_password(self):
        self.with_new_user()
        data = self.get_mock_delete_account_data()
        del data['password']
        self.assert_settings_delete_account_POST_response(data, 400)

    def test_settings_delete_account_POST_incorrect_password(self):
        self.with_new_user()
        data = self.get_mock_delete_account_data(password='wrong')
        self.assert_settings_delete_account_POST_response(data, 400)

    def test_settings_delete_account_POST_success(self):
        user, password = self.with_new_user()
        self.login(email=user.email, password=password)
        data = self.get_mock_delete_account_data(password=password)
        self.assert_settings_delete_account_POST_response(data, 302)

    @mock.patch('dawdle.blueprints.user.mail')
    def test_settings_delete_account_POST_error_sending_email(self, mail_mock):
        mail_mock.send.side_effect = RuntimeError('some error')
        user, password = self.with_new_user()
        data = self.get_mock_delete_account_data(password=password)
        self.assert_settings_delete_account_POST_response(data, 302)
