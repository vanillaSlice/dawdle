import json

from bson.objectid import ObjectId
from flask import url_for

from dawdle.components.board.models import Board
from dawdle.components.column.models import Column
from tests.test_base import TestBase


class TestColumn(TestBase):

    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.board = cls.create_board()

    #
    # index_POST tests.
    #

    def test_index_POST_no_board_id(self):
        data = self._get_mock_create_column_data()
        self._assert_index_POST_bad_request(data, 'Bad Request')

    def test_index_POST_board_does_not_exist(self):
        data = self._get_mock_create_column_data()
        self._assert_index_POST_not_found(data, ObjectId())

    def test_index_POST_not_authenticated(self):
        self.logout()
        data = self._get_mock_create_column_data()
        self._assert_index_POST_forbidden(data, self.board.id)

    def test_index_POST_user_without_permissions(self):
        data = self._get_mock_create_column_data()
        board = self.create_board(owner_id=ObjectId())
        self._assert_index_POST_forbidden(data, board.id)

    def test_index_POST_no_name(self):
        data = self._get_mock_create_column_data()
        del data['name']
        self._assert_index_POST_bad_request(
            data,
            'Please enter a column name',
            board_id=self.board.id,
        )

    def test_index_POST_name_equal_to_min(self):
        name = self.fake.pystr(min_chars=1, max_chars=1)
        data = self._get_mock_create_column_data(name=name)
        self._assert_index_POST_ok(data, self.board.id)

    def test_index_POST_name_equal_to_max(self):
        name = self.fake.pystr(min_chars=256, max_chars=256)
        data = self._get_mock_create_column_data(name=name)
        self._assert_index_POST_ok(data, self.board.id)

    def test_index_POST_name_greater_than_max(self):
        name = self.fake.pystr(min_chars=257, max_chars=257)
        data = self._get_mock_create_column_data(name=name)
        self._assert_index_POST_bad_request(
            data,
            'Column name must be between 1 and 256 characters',
            board_id=self.board.id,
        )

    def _get_mock_create_column_data(self, **kwargs):
        return {
            'name': kwargs.get('name', self.fake.sentence()),
        }

    def _send_index_POST_request(self, data, board_id=None):
        if board_id:
            url = url_for('column.index_POST', board_id=board_id)
        else:
            url = url_for('column.index_POST')
        return self.client.post(url, data=data)

    def _assert_index_POST_ok(self, data, board_id):
        response = self._send_index_POST_request(data, board_id)
        response_json = json.loads(response.data.decode())
        board = Board.objects(id=board_id).first()
        column = Column.objects(id=response_json['id']).first()
        assert response.status_code == 201
        assert column in board.columns
        assert column.board_id == board.id
        assert column.created
        assert column.created_by == self.user.id
        assert column.name == data['name']

    def _assert_index_POST_bad_request(self,
                                       data,
                                       expected_text,
                                       board_id=None):
        response = self._send_index_POST_request(data, board_id)
        assert response.status_code == 400
        assert expected_text.encode() in response.data

    def _assert_index_POST_forbidden(self, data, board_id):
        response = self._send_index_POST_request(data, board_id)
        assert response.status_code == 403
        assert b'Not Authorised' in response.data

    def _assert_index_POST_not_found(self, data, board_id):
        response = self._send_index_POST_request(data, board_id)
        assert response.status_code == 404
        assert b'Not Found' in response.data
