from unittest import mock

from flask import url_for

from tests.test_base import TestBase


class TestContact(TestBase):

    #
    # index_GET tests.
    #

    def test_index_GET(self):
        response = self.client.get(url_for('contact.index_GET'))
        assert response.status_code == 200

    #
    # index_POST tests.
    #

    def test_index_POST_no_email_not_authenticated(self):
        self.logout()
        data = self._get_mock_contact_data()
        del data['email']
        self._assert_index_POST_response(data, 400)

    def test_index_POST_no_email(self):
        data = self._get_mock_contact_data()
        del data['email']
        self._assert_index_POST_response(data, 302)

    def test_index_POST_no_subject(self):
        data = self._get_mock_contact_data()
        del data['subject']
        self._assert_index_POST_response(data, 400)

    def test_index_POST_subject_length_equal_to_minimum(self):
        subject = self.fake.pystr(min_chars=1, max_chars=1)
        data = self._get_mock_contact_data(subject=subject)
        self._assert_index_POST_response(data, 302)

    def test_index_POST_subject_length_equal_to_maximum(self):
        subject = self.fake.pystr(min_chars=256, max_chars=256)
        data = self._get_mock_contact_data(subject=subject)
        self._assert_index_POST_response(data, 302)

    def test_index_POST_subject_length_greater_than_maximum(self):
        subject = self.fake.pystr(min_chars=257, max_chars=257)
        data = self._get_mock_contact_data(subject=subject)
        self._assert_index_POST_response(data, 400)

    def test_index_POST_no_message(self):
        data = self._get_mock_contact_data()
        del data['message']
        self._assert_index_POST_response(data, 400)

    def test_index_POST_message_length_equal_to_minimum(self):
        message = self.fake.pystr(min_chars=1, max_chars=1)
        data = self._get_mock_contact_data(message=message)
        self._assert_index_POST_response(data, 302)

    def test_index_POST_message_length_equal_to_maximum(self):
        message = self.fake.pystr(min_chars=1000, max_chars=1000)
        data = self._get_mock_contact_data(message=message)
        self._assert_index_POST_response(data, 302)

    def test_index_POST_message_length_greater_than_maximum(self):
        message = self.fake.pystr(min_chars=1001, max_chars=1001)
        data = self._get_mock_contact_data(message=message)
        self._assert_index_POST_response(data, 400)

    @mock.patch('dawdle.utils.mail')
    def test_index_POST_error_sending_email(self, mail_mock):
        mail_mock.send.side_effect = RuntimeError('some error')
        data = self._get_mock_contact_data()
        self._assert_index_POST_response(data, 500)

    def test_index_POST_success(self):
        data = self._get_mock_contact_data()
        self._assert_index_POST_response(data, 302)

    def _get_mock_contact_data(self, **kwargs):
        return {
            'email': kwargs.get('email', self.fake.email()),
            'subject': kwargs.get('subject', self.fake.sentence()),
            'message': kwargs.get('message', self.fake.sentences()),
        }

    def _assert_index_POST_response(self, data, status_code):
        response = self.client.post(url_for('contact.index_POST'), data=data)
        assert response.status_code == status_code
