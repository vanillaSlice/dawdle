import json

from bson.objectid import ObjectId
from flask import url_for

from dawdle.models.board import Board, BoardType
from dawdle.utils import get_owner_from_id
from tests.test_base import TestBase


class TestBoard(TestBase):

    #
    # index_POST tests.
    #

    def test_index_POST_not_authenticated(self):
        self.logout()
        data = self._get_mock_create_board_data()
        response = self._send_index_POST_request(data)
        assert response.status_code == 200
        assert b'Log In to Dawdle' in response.data

    def test_index_POST_no_name(self):
        data = self._get_mock_create_board_data()
        del data['name']
        self._assert_index_POST_bad_request(data, 'Please enter a board name')

    def test_index_POST_name_equal_to_min(self):
        name = self.fake.pystr(min_chars=1, max_chars=1)
        data = self._get_mock_create_board_data(name=name)
        self._assert_index_POST_ok(data)

    def test_index_POST_name_equal_to_max(self):
        name = self.fake.pystr(min_chars=256, max_chars=256)
        data = self._get_mock_create_board_data(name=name)
        self._assert_index_POST_ok(data)

    def test_index_POST_name_greater_than_max(self):
        name = self.fake.pystr(min_chars=257, max_chars=257)
        data = self._get_mock_create_board_data(name=name)
        self._assert_index_POST_bad_request(
            data,
            'Board name must be between 1 and 256 characters',
        )

    def test_index_POST_no_owner_id(self):
        data = self._get_mock_create_board_data()
        del data['owner_id']
        self._assert_index_POST_bad_request(data, 'Please enter an owner ID')

    def test_index_POST_personal_type_not_owner(self):
        owner_id = ObjectId()
        data = self._get_mock_create_board_data(owner_id=owner_id)
        self._assert_index_POST_bad_request(
            data,
            'Not authorised to create board with given owner ID',
        )

    def test_index_POST_no_type(self):
        data = self._get_mock_create_board_data()
        del data['type']
        self._assert_index_POST_bad_request(data, 'Not a valid choice')

    def test_index_POST_invalid_type(self):
        data = self._get_mock_create_board_data(type='invalid')
        self._assert_index_POST_bad_request(data, 'Not a valid choice')

    def test_index_POST_success(self):
        name = self.fake.pystr()
        data = self._get_mock_create_board_data(name=name)
        self._assert_index_POST_ok(data)

    def _get_mock_create_board_data(self, **kwargs):
        return {
            'name': kwargs.get('name', self.fake.sentence()),
            'owner_id': kwargs.get('owner_id', str(self.user.id)),
            'type': kwargs.get('type', BoardType.PERSONAL.id),
        }

    def _send_index_POST_request(self, data):
        return self.client.post(
            url_for('board.index_POST'),
            data=data,
            follow_redirects=True,
        )

    def _assert_index_POST_ok(self, data):
        response = self._send_index_POST_request(data)
        response_json = json.loads(response.data.decode())
        board = Board.objects(id=response_json['id']).first()
        owner = get_owner_from_id(data['owner_id'])
        assert response.status_code == 201
        assert response_json['name'] == data['name']
        assert board.created_by == self.user.id
        assert board.name == data['name']
        assert str(board.owner_id) == data['owner_id']
        assert board.type == data['type']
        assert board in owner.boards

    def _assert_index_POST_bad_request(self, data, expected_text):
        response = self._send_index_POST_request(data)
        assert response.status_code == 400
        assert expected_text.encode() in response.data
