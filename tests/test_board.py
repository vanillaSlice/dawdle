import json

from flask import url_for
from bson.objectid import ObjectId

from dawdle.models.board import Board, BoardType, BoardVisibility
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
        assert response.status_code == 401
        assert b'Could not create board' in response.data

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

    def test_index_POST_no_owner(self):
        data = self._get_mock_create_board_data()
        data['owner'] = ''
        self._assert_index_POST_bad_request(data, 'Please select board owner')

    def test_index_POST_no_visibility(self):
        data = self._get_mock_create_board_data()
        data['visibility'] = ''
        self._assert_index_POST_bad_request(
            data,
            'Please select board visibility',
        )

    def test_index_POST_invalid_visibility(self):
        data = self._get_mock_create_board_data(visibility='invalid')
        self._assert_index_POST_bad_request(data, 'Not a valid choice')

    def test_index_POST_success(self):
        name = self.fake.pystr()
        data = self._get_mock_create_board_data(name=name)
        self._assert_index_POST_ok(data)

    def _get_mock_create_board_data(self, **kwargs):
        return {
            'name': kwargs.get('name', self.fake.sentence()),
            'owner': kwargs.get('owner', str(self.user.id)),
            'visibility': kwargs.get('visibility', BoardVisibility.PRIVATE.id),
        }

    def _send_index_POST_request(self, data):
        return self.client.post(
            url_for('board.index_POST'),
            data=data,
            follow_redirects=True,
        )

    def _assert_index_POST_ok(self, data, expected_type=BoardType.PERSONAL):
        response = self._send_index_POST_request(data)
        response_json = json.loads(response.data.decode())
        board = Board.objects(id=response_json['id']).first()
        owner = get_owner_from_id(data['owner'])
        assert response.status_code == 201
        assert response_json['url'] == '/board/{}'.format(board.id)
        assert board.created_by == self.user.id
        assert board.name == data['name']
        assert str(board.owner_id) == data['owner']
        assert board.type == expected_type.id
        assert board.visibility == data['visibility']
        assert board in owner.boards

    def _assert_index_POST_bad_request(self, data, expected_text):
        response = self._send_index_POST_request(data)
        assert response.status_code == 400
        assert expected_text.encode() in response.data

    #
    # board_GET tests.
    #

    def test_board_GET_board_does_not_exist(self):
        self._assert_board_GET_not_found(ObjectId())

    def test_board_GET_not_authenticated(self):
        self.logout()
        board = self.create_board()
        self._assert_board_GET_forbidden(board.id)

    def test_board_GET_user_without_permissions(self):
        board = self.create_board()
        user, _ = self.as_new_user()
        self._assert_board_GET_forbidden(board.id)

    def test_board_GET_success(self):
        board = self.create_board(owner_id=self.user.id)
        self._assert_board_GET_ok(board.id)

    def _send_board_GET_request(self, board_id):
        return self.client.get(
            url_for('board.board_GET', board_id=str(board_id)),
        )

    def _assert_board_GET_ok(self, board_id):
        response = self._send_board_GET_request(board_id)
        board = Board.objects(id=board_id).first()
        assert response.status_code == 200
        assert board.name.encode() in response.data

    def _assert_board_GET_forbidden(self, board_id):
        response = self._send_board_GET_request(board_id)
        assert response.status_code == 403
        assert b'Not Authorised' in response.data

    def _assert_board_GET_not_found(self, board_id):
        response = self._send_board_GET_request(board_id)
        assert response.status_code == 404
        assert b'Not Found' in response.data
