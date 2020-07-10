from dawdle.extensions.marshmallow import trim_string


class TestMarshmallow:

    def test_trim_string_not_present(self):
        data = {}
        trim_string(data, "name")
        assert "name" not in data

    def test_trim_string_not_string(self):
        data = {"name": 1}
        trim_string(data, "name")
        assert data["name"] == 1

    def test_trim_string_blank_string(self):
        data = {"name": " "}
        trim_string(data, "name")
        assert "name" not in data

    def test_trim_string(self):
        data = {"name": "  John   Smith  "}
        trim_string(data, "name")
        assert data["name"] == "John Smith"
