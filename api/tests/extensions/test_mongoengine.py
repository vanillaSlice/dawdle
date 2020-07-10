from bson.objectid import ObjectId

from dawdle.extensions.mongoengine import to_ObjectId


class TestMongoengine:

    def test_to_ObjectId_None(self):
        object_id = to_ObjectId(None)
        assert isinstance(object_id, ObjectId)

    def test_to_ObjectId_invalid(self):
        object_id = to_ObjectId("invalid")
        assert isinstance(object_id, ObjectId)

    def test_to_ObjectId_string(self):
        string = "5f04b7ba96f5ca591762581f"
        object_id = to_ObjectId(string)
        assert object_id == ObjectId(string)

    def test_to_ObjectId_ObjectId(self):
        object_id_a = ObjectId()
        object_id_b = to_ObjectId(object_id_a)
        assert object_id_a == object_id_b
