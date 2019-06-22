from unittest import mock

from flask import url_for

from dawdle.models.user import User
from tests.test_base import TestBase


class TestUser(TestBase):

    #
    # boards_GET tests.
    #

    def test_boards_GET_not_authenticated(self):
        self.logout()
        self._assert_boards_GET_response(302)

    def test_boards_GET(self):
        self._assert_boards_GET_response(200)

    def _assert_boards_GET_response(self, status_code):
        response = self.client.get(url_for('user.boards_GET'))
        assert response.status_code == status_code

    #
    # settings_GET tests.
    #

    def test_settings_GET_not_authenticated(self):
        self.logout()
        self._assert_settings_GET_response(302)

    def test_settings_GET(self):
        self._assert_settings_GET_response(302)

    def _assert_settings_GET_response(self, status_code):
        response = self.client.get(url_for('user.settings_GET'))
        assert response.status_code == status_code

    #
    # settings_account_details_GET tests.
    #

    def test_settings_account_details_GET_not_authenticated(self):
        self.logout()
        self._assert_settings_account_details_GET_response(302)

    def test_settings_account_details_GET(self):
        self._assert_settings_account_details_GET_response(200)

    def _assert_settings_account_details_GET_response(self, status_code):
        response = self.client.get(
            url_for('user.settings_account_details_GET'),
        )
        assert response.status_code == status_code

    #
    # settings_account_details_POST tests.
    #

    def test_settings_account_details_POST_name_equal_to_min(self):
        name = self.fake.pystr(min_chars=1, max_chars=1)
        data = self._get_mock_account_details_data(name=name)
        self._assert_settings_account_details_POST_successful(data)

    def test_settings_account_details_POST_name_equal_to_max(self):
        name = self.fake.pystr(min_chars=50, max_chars=50)
        data = self._get_mock_account_details_data(name=name)
        self._assert_settings_account_details_POST_successful(data)

    def test_settings_account_details_POST_name_greater_than_max(self):
        name = self.fake.pystr(min_chars=51, max_chars=51)
        data = self._get_mock_account_details_data(name=name)
        self._assert_settings_account_details_POST_unsuccessful(data)

    def test_settings_account_details_POST_initials_equal_to_min(self):
        initials = self.fake.pystr(min_chars=1, max_chars=1)
        data = self._get_mock_account_details_data(initials=initials)
        self._assert_settings_account_details_POST_successful(data)

    def test_settings_account_details_POST_initials_equal_to_max(self):
        initials = self.fake.pystr(min_chars=4, max_chars=4)
        data = self._get_mock_account_details_data(initials=initials)
        self._assert_settings_account_details_POST_successful(data)

    def test_settings_account_details_POST_initials_greater_than_max(self):
        initials = self.fake.pystr(min_chars=5, max_chars=5)
        data = self._get_mock_account_details_data(initials=initials)
        self._assert_settings_account_details_POST_unsuccessful(data)

    def test_settings_account_details_POST_no_update(self):
        user, password = self.as_new_user()
        data = self._get_mock_account_details_data(
            name=user.name,
            initials=user.initials,
        )
        self._assert_settings_account_details_POST_no_update(user.id, data)

    def test_settings_account_details_POST_success(self):
        data = self._get_mock_account_details_data()
        self._assert_settings_account_details_POST_successful(data)

    def _get_mock_account_details_data(self, **kwargs):
        return {
            'name': kwargs.get('name', self.fake.name()),
            'initials': kwargs.get(
                'initials',
                self.fake.pystr(min_chars=1, max_chars=4),
            ),
        }

    def _assert_settings_account_details_POST_successful(self, data):
        user, password = self.as_new_user()
        response = self.client.post(
            url_for('user.settings_account_details_POST'),
            data=data,
        )
        user = User.objects(id=user.id).first()
        assert response.status_code == 302
        assert user.initials == data['initials']
        assert user.last_updated
        assert user.name == data['name']

    def _assert_settings_account_details_POST_unsuccessful(self, data):
        user, password = self.as_new_user()
        response = self.client.post(
            url_for('user.settings_account_details_POST'),
            data=data,
        )
        user = User.objects(id=user.id).first()
        assert response.status_code == 400
        assert not user.last_updated

    def _assert_settings_account_details_POST_no_update(self, user_id, data):
        response = self.client.post(
            url_for('user.settings_account_details_POST'),
            data=data,
        )
        user = User.objects(id=user_id).first()
        assert response.status_code == 302
        assert user.initials == data['initials']
        assert not user.last_updated
        assert user.name == data['name']

    #
    # settings_update_email_GET tests.
    #

    def test_settings_update_email_GET_not_authenticated(self):
        self.logout()
        self._assert_settings_update_email_GET_response(302)

    def test_settings_update_email_GET(self):
        self._assert_settings_update_email_GET_response(200)

    def _assert_settings_update_email_GET_response(self, status_code):
        response = self.client.get(url_for('user.settings_update_email_GET'))
        assert response.status_code == status_code

    #
    # settings_update_email_POST tests.
    #

    def test_settings_update_email_POST_not_authenticated(self):
        self.logout()
        response = self.client.post(url_for('user.settings_update_email_POST'))
        assert response.status_code == 302

    def test_settings_update_email_POST_invalid_email(self):
        user, password = self.as_new_user()
        email = self.fake.sentence()
        data = self._get_mock_update_email_data(email=email, password=password)
        self._assert_settings_update_email_POST_unsuccessful(
            user.id,
            user.auth_id,
            data,
        )

    def test_settings_update_email_POST_incorrect_password(self):
        user, password = self.as_new_user()
        email = self.fake.email()
        data = self._get_mock_update_email_data(email=email, password='wrong')
        self._assert_settings_update_email_POST_unsuccessful(
            user.id,
            user.auth_id,
            data,
        )

    def test_settings_update_email_POST_account_already_exists(self):
        user, password = self.as_new_user()
        email = self.user.email
        data = self._get_mock_update_email_data(email=email, password=password)
        self._assert_settings_update_email_POST_unsuccessful(
            user.id,
            user.auth_id,
            data,
        )

    def test_settings_update_email_POST_no_update(self):
        user, password = self.as_new_user()
        email = user.email
        data = self._get_mock_update_email_data(email=email, password=password)
        self._assert_settings_update_email_POST_no_update(
            user.id,
            user.auth_id,
            data,
        )

    def test_settings_update_email_POST_success(self):
        user, password = self.as_new_user()
        email = self.fake.email()
        data = self._get_mock_update_email_data(email=email, password=password)
        self._assert_settings_update_email_POST_successful(
            user.id,
            user.auth_id,
            data,
        )

    def _get_mock_update_email_data(self, **kwargs):
        return {
            'email': kwargs.get('email', self.fake.email()),
            'password': kwargs.get('password', self.fake.password()),
        }

    def _assert_settings_update_email_POST_successful(self,
                                                      user_id,
                                                      auth_id,
                                                      data):
        response = self.client.post(
            url_for('user.settings_update_email_POST'),
            data=data,
        )
        user = User.objects(id=user_id).first()
        assert response.status_code == 302
        assert not user.is_active
        assert user.auth_id != auth_id
        assert user.email == data['email']
        assert user.last_updated

    def _assert_settings_update_email_POST_unsuccessful(self,
                                                        user_id,
                                                        auth_id,
                                                        data):
        response = self.client.post(
            url_for('user.settings_update_email_POST'),
            data=data,
        )
        user = User.objects(id=user_id).first()
        assert response.status_code == 400
        assert user.is_active
        assert user.auth_id == auth_id
        assert user.email != data['email']
        assert not user.last_updated

    def _assert_settings_update_email_POST_no_update(self,
                                                     user_id,
                                                     auth_id,
                                                     data):
        response = self.client.post(
            url_for('user.settings_update_email_POST'),
            data=data,
        )
        user = User.objects(id=user_id).first()
        assert response.status_code == 302
        assert user.is_active
        assert user.auth_id == auth_id
        assert user.email == data['email']
        assert not user.last_updated

    #
    # settings_update_password_GET tests.
    #

    def test_settings_update_password_GET_not_authenticated(self):
        self.logout()
        self._assert_settings_update_password_GET_response(302)

    def test_settings_update_password_GET(self):
        self._assert_settings_update_password_GET_response(200)

    def _assert_settings_update_password_GET_response(self, status_code):
        response = self.client.get(
            url_for('user.settings_update_password_GET'),
        )
        assert response.status_code == status_code

    #
    # settings_update_password_POST tests.
    #

    def test_settings_update_password_POST_not_authenticated(self):
        self.logout()
        response = self.client.post(
            url_for('user.settings_update_password_POST'),
        )
        assert response.status_code == 302

    def test_settings_update_password_POST_incorrect_current_password(self):
        user, password = self.as_new_user()
        current_password = 'wrong'
        new_password = self.fake.password()
        confirmation = new_password
        data = self._get_mock_update_password_data(
            current_password=current_password,
            new_password=new_password,
            confirmation=confirmation,
        )
        self._assert_settings_update_password_POST_unsuccessful(
            user.auth_id,
            data,
        )

    def test_settings_update_password_POST_new_password_less_than_min(self):
        user, password = self.as_new_user()
        current_password = password
        new_password = self.fake.pystr(min_chars=7, max_chars=7)
        confirmation = new_password
        data = self._get_mock_update_password_data(
            current_password=current_password,
            new_password=new_password,
            confirmation=confirmation,
        )
        self._assert_settings_update_password_POST_unsuccessful(
            user.auth_id,
            data,
        )

    def test_settings_update_password_POST_new_password_equal_to_min(self):
        user, password = self.as_new_user()
        current_password = password
        new_password = self.fake.pystr(min_chars=8, max_chars=8)
        confirmation = new_password
        data = self._get_mock_update_password_data(
            current_password=current_password,
            new_password=new_password,
            confirmation=confirmation,
        )
        self._assert_settings_update_password_POST_successful(
            user.id,
            user.auth_id,
            data,
        )

    def test_settings_update_password_POST_dont_match(self):
        user, password = self.as_new_user()
        current_password = password
        new_password = self.fake.password()
        confirmation = 'wrong'
        data = self._get_mock_update_password_data(
            current_password=current_password,
            new_password=new_password,
            confirmation=confirmation,
        )
        self._assert_settings_update_password_POST_unsuccessful(
            user.auth_id,
            data,
        )

    def test_settings_update_password_POST_no_update(self):
        user, password = self.as_new_user()
        current_password = password
        new_password = password
        confirmation = password
        data = self._get_mock_update_password_data(
            current_password=current_password,
            new_password=new_password,
            confirmation=confirmation,
        )
        self._assert_settings_update_password_POST_no_update(
            user.id,
            user.auth_id,
            data,
        )

    def test_settings_update_password_POST_success(self):
        user, password = self.as_new_user()
        current_password = password
        new_password = self.fake.password()
        confirmation = new_password
        data = self._get_mock_update_password_data(
            current_password=current_password,
            new_password=new_password,
            confirmation=confirmation,
        )
        self._assert_settings_update_password_POST_successful(
            user.id,
            user.auth_id,
            data,
        )

    def _get_mock_update_password_data(self, **kwargs):
        return {
            'current_password': kwargs.get(
                'current_password',
                self.fake.password(),
            ),
            'new_password': kwargs.get('new_password', self.fake.password()),
            'confirmation': kwargs.get('confirmation', self.fake.password()),
        }

    def _assert_settings_update_password_POST_successful(self,
                                                         user_id,
                                                         auth_id,
                                                         data):
        response = self.client.post(
            url_for('user.settings_update_password_POST'),
            data=data,
        )
        user = User.objects(id=user_id).first()
        assert response.status_code == 302
        assert user.auth_id != auth_id
        assert user.last_updated
        assert user.verify_password(data['new_password'])

    def _assert_settings_update_password_POST_unsuccessful(self,
                                                           auth_id,
                                                           data):
        response = self.client.post(
            url_for('user.settings_update_password_POST'),
            data=data,
        )
        user = User.objects(auth_id=auth_id).first()
        assert response.status_code == 400
        assert not user.last_updated

    def _assert_settings_update_password_POST_no_update(self,
                                                        user_id,
                                                        auth_id,
                                                        data):
        response = self.client.post(
            url_for('user.settings_update_password_POST'),
            data=data,
        )
        user = User.objects(id=user_id).first()
        assert response.status_code == 302
        assert user.auth_id == auth_id
        assert not user.last_updated
        assert user.verify_password(data['current_password'])

    #
    # settings_delete_account_GET tests.
    #

    def test_settings_delete_account_GET_not_authenticated(self):
        self.logout()
        self._assert_settings_delete_account_GET_response(302)

    def test_settings_delete_account_GET(self):
        self._assert_settings_delete_account_GET_response(200)

    def _assert_settings_delete_account_GET_response(self, status_code):
        response = self.client.get(url_for('user.settings_delete_account_GET'))
        assert response.status_code == status_code

    #
    # settings_delete_account_POST tests.
    #

    def test_settings_delete_account_POST_not_authenticated(self):
        self.logout()
        data = self._get_mock_delete_account_data()
        self._assert_settings_delete_account_POST_response(data, 302)

    def test_settings_delete_account_POST_no_password(self):
        self.as_new_user()
        data = self._get_mock_delete_account_data()
        del data['password']
        self._assert_settings_delete_account_POST_response(data, 400)

    def test_settings_delete_account_POST_incorrect_password(self):
        self.as_new_user()
        data = self._get_mock_delete_account_data(password='wrong')
        self._assert_settings_delete_account_POST_response(data, 400)

    def test_settings_delete_account_POST_success(self):
        user, password = self.as_new_user()
        self.login(email=user.email, password=password)
        data = self._get_mock_delete_account_data(password=password)
        self._assert_settings_delete_account_POST_response(data, 302)

    @mock.patch('dawdle.utils.mail')
    def test_settings_delete_account_POST_error_sending_email(self, mail_mock):
        mail_mock.send.side_effect = RuntimeError('some error')
        user, password = self.as_new_user()
        data = self._get_mock_delete_account_data(password=password)
        self._assert_settings_delete_account_POST_response(data, 302)

    def _get_mock_delete_account_data(self, **kwargs):
        return {'password': kwargs.get('password', self.fake.password())}

    def _assert_settings_delete_account_POST_response(self, data, status_code):
        response = self.client.post(
            url_for('user.settings_delete_account_POST'),
            data=data,
        )
        assert response.status_code == status_code
