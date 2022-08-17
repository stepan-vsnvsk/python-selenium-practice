import json


class JsonUtils:
    """Functions to work with json formatted data."""

    @staticmethod
    def read_from_json(json_data: json):
        """Read json file."""
        with open(json_data, 'r') as json_file:
            data_load = json.loads(json_file.read())
            return data_load

    @staticmethod
    def check_is_that_json(data_to_check):
        try:
            json.loads(data_to_check)
        except ValueError:
            return False
        return True
