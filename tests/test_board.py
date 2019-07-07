from flask import url_for

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
        board_in_response = Board.from_json(response.data.decode())
        board_saved = Board.objects(id=board_in_response.id).first()
        owner = get_owner_from_id(data['owner'])
        assert response.status_code == 201
        assert board_in_response == board_saved
        assert board_saved.created_by == self.user.id
        assert board_saved.name == data['name']
        assert str(board_saved.owner_id) == data['owner']
        assert board_saved.type == expected_type.id
        assert board_saved.visibility == data['visibility']
        assert board_saved in owner.boards

    def _assert_index_POST_bad_request(self, data, expected_text):
        response = self._send_index_POST_request(data)
        assert response.status_code == 400
        assert expected_text.encode() in response.data
