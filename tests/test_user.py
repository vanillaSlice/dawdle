from flask import url_for

from dawdle.models.user import User
from tests.test_base import fake, TestBase

class TestUser(TestBase):

    #
    # Utils
    #

    def get_mock_update_password_data(self,
                                      current_password=fake.password,
                                      new_password=fake.password,
                                      confirmation=fake.password):
        return {
            'current_password': current_password() if callable(current_password) else current_password,
            'new_password': new_password() if callable(new_password) else new_password,
            'confirmation': confirmation() if callable(confirmation) else confirmation,
        }

    #
    # boards_GET tests.
    #

    def test_boards_GET_not_authenticated(self):
        self.logout()
        response = self.client.get(url_for('user.boards_GET'))
        assert response.status_code == 302

    def test_boards_GET_authenticated(self):
        response = self.client.get(url_for('user.boards_GET'))
        assert response.status_code == 200

    #
    # settings_GET tests.
    #

    def test_settings_GET_not_authenticated(self):
        self.logout()
        response = self.client.get(url_for('user.settings_GET'))
        assert response.status_code == 302

    def test_settings_GET_authenticated(self):
        response = self.client.get(url_for('user.settings_GET'))
        assert response.status_code == 302

    #
    # settings_update_password_GET tests.
    #

    def test_settings_update_password_GET_not_authenticated(self):
        self.logout()
        response = self.client.get(url_for('user.settings_update_password_GET'))
        assert response.status_code == 302

    def test_settings_update_password_GET_authenticated(self):
        response = self.client.get(url_for('user.settings_update_password_GET'))
        assert response.status_code == 200

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
        current_password = 'wrong'
        new_password = fake.pystr(min_chars=8, max_chars=8)
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_unsuccessful(self.user.auth_id, data)

    def test_settings_update_password_POST_new_password_length_less_than_minimum(self):
        current_password = self.password
        new_password = fake.pystr(min_chars=7, max_chars=7)
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_unsuccessful(self.user.auth_id, data)

    def test_settings_update_password_POST_new_password_length_equal_to_minimum(self):
        current_password = self.password
        new_password = fake.pystr(min_chars=8, max_chars=8)
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_successful(self.user.id, self.user.auth_id, data)

    def test_settings_update_password_POST_new_password_and_confirmation_dont_match(self):
        current_password = self.password
        new_password = fake.pystr(min_chars=8, max_chars=8)
        confirmation = 'wrong'
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_unsuccessful(self.user.auth_id, data)

    def test_settings_update_password_POST_success(self):
        current_password = self.password
        new_password = fake.pystr(min_chars=8, max_chars=8)
        confirmation = new_password
        data = self.get_mock_update_password_data(current_password=current_password,
                                                  new_password=new_password,
                                                  confirmation=confirmation)
        self.assert_settings_update_password_POST_successful(self.user.id, self.user.auth_id, data)

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

    def test_settings_delete_account_POST_not_authenticated(self):
        self.logout()
        response = self.client.post(url_for('user.settings_delete_account_POST'))
        assert response.status_code == 302
        assert len(User.objects()) == 1

    def test_settings_delete_account_POST_authenticated(self):
        response = self.client.post(url_for('user.settings_delete_account_POST'))
        assert response.status_code == 302
        assert not User.objects()
