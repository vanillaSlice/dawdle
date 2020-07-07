from datetime import datetime

from bson.objectid import ObjectId

from dawdle.components.user.models import User


class TestModels:

    def test_User_defaults(self):
        user = User()
        assert not user.active
        assert isinstance(user.auth_id, ObjectId)
        assert isinstance(user.created, datetime)
        assert not user.email
        assert not user.initials
        assert isinstance(user.last_updated, datetime)
        assert not user.name
        assert not user.password
