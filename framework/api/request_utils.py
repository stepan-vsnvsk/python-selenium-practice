import requests
from framework.utils.logger import Logger as log


class MakeRequestUtils:
    """Utility functions to work with request/response."""

    @staticmethod
    def check_is_code_ok(status_code):
        log.info(f"Check whether request was successfull")
        return status_code == requests.codes.ok
        