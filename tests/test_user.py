from unittest import mock

from flask import url_for

from dawdle.models.user import Board, User
from tests.test_base import TestBase


class TestUser(TestBase):

    def test_boards_GET(self):
        def ok(expected_text):
            response = self.client.get(
                url_for('user.boards_GET'),
                follow_redirects=True,
            )
            assert response.status_code == 200
            assert expected_text.encode() in response.data

        # not authenticated
        self.logout()
        ok('Log In | Dawdle')

        # authenticated
        self.login()
        ok('Boards | Dawdle')

    def test_settings_GET(self):
        def ok(expected_text):
            response = self.client.get(
                url_for('user.settings_GET'),
                follow_redirects=True,
            )
            assert response.status_code == 200
            assert expected_text.encode() in response.data

        # not authenticated
        self.logout()
        ok('Log In | Dawdle')

        # authenticated
        self.login()
        ok('Account Details | Dawdle')

    def test_settings_account_details_GET(self):
        def ok(expected_text):
            response = self.client.get(
                url_for('user.settings_account_details_GET'),
                follow_redirects=True,
            )
            assert response.status_code == 200
            assert expected_text.encode() in response.data

        # not authenticated
        self.logout()
        ok('Log In | Dawdle')

        # authenticated
        self.login()
        ok('Account Details | Dawdle')

    def test_settings_account_details_POST(self):
        def mock_data(**kwargs):
            return {
                'name': kwargs.get('name', self.fake.name()),
                'initials': kwargs.get(
                    'initials',
                    self.fake.pystr(min_chars=1, max_chars=4),
                ),
            }

        def send_request(data):
            return self.client.post(
                url_for('user.settings_account_details_POST'),
                data=data,
                follow_redirects=True,
            )

        def ok(user_id, data, updated=True):
            response = send_request(data)
            user = User.objects(id=user_id).first()
            assert response.status_code == 200
            assert user.initials == data['initials']
            assert user.name == data['name']
            if updated:
                assert b'Your account details have been updated' in \
                    response.data
            else:
                assert b'No update needed' in response.data

        def bad_request(user_id, data, expected_text):
            response = send_request(data)
            user = User.objects(id=user_id).first()
            assert response.status_code == 400
            assert expected_text.encode() in response.data
            assert user.initials != data['initials']
            assert user.name != data['name']

        # not authenticated
        self.logout()
        response = send_request(mock_data())
        assert response.status_code == 200
        assert b'Log In | Dawdle' in response.data

        # name has min chars
        user, _ = self.as_new_user()
        name = self.fake.pystr(min_chars=1, max_chars=1)
        data = mock_data(name=name)
        ok(user.id, data)

        # name has max chars
        name = self.fake.pystr(min_chars=50, max_chars=50)
        data = mock_data(name=name)
        ok(user.id, data)

        # name exceeds max chars
        name = self.fake.pystr(min_chars=51, max_chars=51)
        data = mock_data(name=name)
        bad_request(
            user.id,
            data,
            'Your name must be between 1 and 50 characters',
        )

        # initials has min chars
        initials = self.fake.pystr(min_chars=1, max_chars=1)
        data = mock_data(initials=initials)
        ok(user.id, data)

        # initials has max chars
        initials = self.fake.pystr(min_chars=4, max_chars=4)
        data = mock_data(initials=initials)
        ok(user.id, data)

        # initials exceeds max chars
        initials = self.fake.pystr(min_chars=5, max_chars=5)
        data = mock_data(initials=initials)
        bad_request(
            user.id,
            data,
            'Your initials must be between 1 and 4 characters',
        )

        # updates
        data = mock_data()
        ok(user.id, data)

        # no update needed
        ok(user.id, data, updated=False)

    def test_settings_update_email_GET(self):
        def ok(expected_text):
            response = self.client.get(
                url_for('user.settings_update_email_GET'),
                follow_redirects=True,
            )
            assert response.status_code == 200
            assert expected_text.encode() in response.data

        # not authenticated
        self.logout()
        ok('Log In | Dawdle')

        # authenticated
        self.login()
        ok('Update Email | Dawdle')

    def test_settings_update_email_POST(self):
        def mock_data(**kwargs):
            return {
                'email': kwargs.get('email', self.fake.email()),
                'password': kwargs.get('password', self.fake.password()),
            }

        def send_request(data):
            return self.client.post(
                url_for('user.settings_update_email_POST'),
                data=data,
                follow_redirects=True,
            )

        def ok(user_id, auth_id, data, updated=True):
            response = send_request(data)
            user = User.objects(id=user_id).first()
            assert response.status_code == 200
            assert user.email == data['email']
            if updated:
                assert b'A verification email has been sent' in response.data
                assert not user.is_active
                assert user.auth_id != auth_id
            else:
                assert b'No update needed' in response.data
                assert user.is_active
                assert user.auth_id == auth_id

        def bad_request(user_id, auth_id, data, expected_text):
            response = send_request(data)
            user = User.objects(id=user_id).first()
            assert response.status_code == 400
            assert expected_text.encode() in response.data
            assert user.is_active
            assert user.auth_id == auth_id
            assert user.email != data['email']

        # not authenticated
        self.logout()
        data = mock_data()
        response = send_request(data)
        assert response.status_code == 200
        assert b'Log In | Dawdle' in response.data

        # invalid email
        user, password = self.as_new_user()
        email = self.fake.sentence()
        data = mock_data(email=email, password=password)
        bad_request(user.id, user.auth_id, data, 'Please enter a valid email')

        # incorrect password
        email = self.fake.email()
        data = mock_data(email=email, password='wrong')
        bad_request(user.id, user.auth_id, data, 'Incorrect password')

        # account with email exists
        email = self.user.email
        data = mock_data(email=email, password=password)
        bad_request(
            user.id,
            user.auth_id,
            data,
            'There is already an account with this email',
        )

        # no update needed
        email = user.email
        data = mock_data(email=email, password=password)
        ok(user.id, user.auth_id, data, updated=False)

        # updates
        email = self.fake.email()
        data = mock_data(email=email, password=password)
        ok(user.id, user.auth_id, data)

    def test_settings_update_password_GET(self):
        def ok(expected_text):
            response = self.client.get(
                url_for('user.settings_update_password_GET'),
                follow_redirects=True,
            )
            assert response.status_code == 200
            assert expected_text.encode() in response.data

        # not authenticated
        self.logout()
        ok('Log In | Dawdle')

        # authenticated
        self.login()
        ok('Update Password | Dawdle')

    def test_settings_update_password_POST(self):
        def mock_data(**kwargs):
            current_password = kwargs.get(
                'current_password',
                self.fake.password(),
            )
            new_password = kwargs.get(
                'new_password',
                self.fake.password(),
            )
            confirmation = kwargs.get('confirmation', new_password)
            return {
                'current_password': current_password,
                'new_password': new_password,
                'confirmation': confirmation,
            }

        def send_request(data):
            return self.client.post(
                url_for('user.settings_update_password_POST'),
                data=data,
                follow_redirects=True,
            )

        def ok(user_id, auth_id, data, updated=True):
            response = send_request(data)
            user = User.objects(id=user_id).first()
            assert response.status_code == 200
            assert user.verify_password(data['new_password'])
            if updated:
                assert b'Your password has been updated' in response.data
                assert user.auth_id != auth_id
            else:
                assert b'No update needed' in response.data
                assert user.auth_id == auth_id

        def bad_request(auth_id, data, expected_text):
            response = send_request(data)
            user = User.objects(auth_id=auth_id).first()
            assert response.status_code == 400
            assert expected_text.encode() in response.data

        # not authenticated
        self.logout()
        data = mock_data()
        response = send_request(data)
        assert response.status_code == 200
        assert b'Log In | Dawdle' in response.data

        # incorrect current password
        user, password = self.as_new_user()
        data = mock_data(current_password='wrong')
        bad_request(user.auth_id, data, 'Incorrect current password')

        # new password less than min chars
        data = mock_data(
            new_password=self.fake.pystr(min_chars=7, max_chars=7),
        )
        bad_request(
            user.auth_id,
            data,
            'Your new password must be at least 8 characters',
        )

        # new password has min chars
        new_password = self.fake.pystr(min_chars=8, max_chars=8)
        data = mock_data(
            current_password=password,
            new_password=new_password,
        )
        ok(user.id, user.auth_id, data)
        user = User.objects(id=user.id).first()

        # new password and confirmation don't match
        current_password = new_password
        new_password = self.fake.password()
        confirmation = 'wrong'
        data = mock_data(
            current_password=current_password,
            new_password=new_password,
            confirmation=confirmation,
        )
        bad_request(
            user.auth_id,
            data,
            'New password and confirmation must match',
        )

        # no update needed
        data = mock_data(
            current_password=current_password,
            new_password=current_password,
        )
        ok(user.id, user.auth_id, data, updated=False)
        user = User.objects(id=user.id).first()

        # updates
        data = mock_data(current_password=current_password)
        ok(user.id, user.auth_id, data)

    def test_settings_delete_account_GET(self):
        def ok(expected_text):
            response = self.client.get(
                url_for('user.settings_delete_account_GET'),
                follow_redirects=True,
            )
            assert response.status_code == 200
            assert expected_text.encode() in response.data

        # not authenticated
        self.logout()
        ok('Log In | Dawdle')

        # authenticated
        self.login()
        ok('Delete Account | Dawdle')

    def test_settings_delete_account_POST(self):
        def mock_data(**kwargs):
            return {'password': kwargs.get('password', self.fake.password())}

        def send_request(data):
            return self.client.post(
                url_for('user.settings_delete_account_POST'),
                data=data,
                follow_redirects=True,
            )

        def ok(user, data):
            assert Board.objects(owner_id=user.id).count() == len(user.boards)
            response = send_request(data)
            assert response.status_code == 200
            assert b'Your account has been deleted' in response.data
            assert Board.objects(owner_id=user.id).count() == 0

        def bad_request(data, expected_text):
            response = send_request(data)
            assert response.status_code == 400
            assert expected_text.encode() in response.data

        # not authenticated
        self.logout()
        data = mock_data()
        response = send_request(data)
        assert response.status_code == 200
        assert b'Log In | Dawdle' in response.data

        # no password
        user, password = self.as_new_user()
        data = mock_data()
        del data['password']
        bad_request(data, 'Please enter your password')

        # incorrect password
        data = mock_data(password='wrong')
        bad_request(data, 'Incorrect password')

        # deletes
        data = mock_data(password=password)
        ok(user, data)

        # with boards
        user, password = self.as_new_user()
        user.boards = self.create_boards(user.id, max_boards=4)
        user.save()
        data = mock_data(password=password)
        ok(user, data)

        # error sending email
        with mock.patch('dawdle.utils.mail') as mail_mock:
            mail_mock.send.side_effect = RuntimeError('some error')
            user, password = self.as_new_user()
            data = mock_data(password=password)
            ok(user, data)
