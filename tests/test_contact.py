from flask import url_for

from tests.test_base import fake, TestBase

class TestContact(TestBase):

    #
    # Utils
    #

    def get_mock_contact_data(self,
                              email=fake.email,
                              subject=fake.sentence,
                              message=fake.sentences):
        return {
            'email': email() if callable(email) else email,
            'subject': subject() if callable(subject) else subject,
            'message': message() if callable(message) else message,
        }

    #
    # index_GET tests.
    #

    def test_index_GET(self):
        response = self.client.get(url_for('contact.index_GET'))
        assert response.status_code == 200

    #
    # index_POST tests.
    #

    def assert_index_POST_successful(self, data):
        response = self.client.post(url_for('contact.index_POST'), data=data)
        assert response.status_code == 302

    def assert_index_POST_unsuccessful(self, data):
        response = self.client.post(url_for('contact.index_POST'), data=data)
        assert response.status_code == 400

    def test_index_POST_no_email_not_authenticated(self):
        self.logout()
        email = None
        data = self.get_mock_contact_data(email=email)
        self.assert_index_POST_unsuccessful(data)

    def test_index_POST_no_email_authenticated(self):
        email = None
        data = self.get_mock_contact_data(email=email)
        self.assert_index_POST_successful(data)

    def test_index_POST_no_subject(self):
        subject = None
        data = self.get_mock_contact_data(subject=subject)
        self.assert_index_POST_unsuccessful(data)

    def test_index_POST_subject_length_equal_to_minimum(self):
        subject = fake.pystr(min_chars=1, max_chars=1)
        data = self.get_mock_contact_data(subject=subject)
        self.assert_index_POST_successful(data)

    def test_index_POST_subject_length_equal_to_maximum(self):
        subject = fake.pystr(min_chars=256, max_chars=256)
        data = self.get_mock_contact_data(subject=subject)
        self.assert_index_POST_successful(data)

    def test_index_POST_subject_length_greater_than_maximum(self):
        subject = fake.pystr(min_chars=257, max_chars=257)
        data = self.get_mock_contact_data(subject=subject)
        self.assert_index_POST_unsuccessful(data)

    def test_index_POST_no_message(self):
        message = None
        data = self.get_mock_contact_data(message=message)
        self.assert_index_POST_unsuccessful(data)

    def test_index_POST_message_length_equal_to_minimum(self):
        message = fake.pystr(min_chars=1, max_chars=1)
        data = self.get_mock_contact_data(subject=message)
        self.assert_index_POST_successful(data)

    def test_index_POST_message_length_equal_to_maximum(self):
        message = fake.pystr(min_chars=1000, max_chars=1000)
        data = self.get_mock_contact_data(message=message)
        self.assert_index_POST_successful(data)

    def test_index_POST_message_length_greater_than_maximum(self):
        message = fake.pystr(min_chars=1001, max_chars=1001)
        data = self.get_mock_contact_data(message=message)
        self.assert_index_POST_unsuccessful(data)

    def test_index_POST_success(self):
        data = self.get_mock_contact_data()
        self.assert_index_POST_successful(data)
