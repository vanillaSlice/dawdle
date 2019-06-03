from flask import url_for
from flask_login import current_user

from dawdle.models.user import User
from tests.test_base import TestBase

class TestUser(TestBase):

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
        assert response.status_code == 200

    #
    # delete_POST tests.
    #

    def test_delete_POST_not_authenticated(self):
        self.logout()
        response = self.client.post(url_for('user.delete_POST'))
        assert response.status_code == 302
        assert len(User.objects()) == 1

    def test_delete_POST_authenticated(self):
        response = self.client.post(url_for('user.delete_POST'))
        assert response.status_code == 302
        assert not User.objects()
