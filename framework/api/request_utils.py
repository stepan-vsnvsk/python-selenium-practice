import requests
from framework.utils.logger import Logger as log


class MakeRequestUtils:
    """Utility functions to work with request/response."""

    @staticmethod
    def check_status_code(status_code, expected=200):
        log.info(f"Check whether response's status code is {expected} ")
        return int(status_code) == int(expected)