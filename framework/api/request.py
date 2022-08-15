import requests
from framework.utils.logger import Logger as log


class MakeRequest:
    """Wrapper around Requests lib."""

    @staticmethod
    def get(url, params={}, headers={}, auth=None, verify=False):
        """Make a HTTP API GET request.

        Note:
            No cares about exceptions.
        Returns:
            Response object.
        """

        log.info(f"Make HTTP API GET request to {url}")
        return requests.get(url, params=params, headers=headers, auth=auth, verify=verify)        


    @staticmethod
    def post(url, data={}, params={}, headers={}, files=None, auth=None, verify=False):
        """Make a HTTP API POST request.

        Note:
            No cares about exceptions.
        Returns:
            Response object.
        """

        log.info(f"Make HTTP API POST request to {url}")
        return requests.post(url, data=data, params=params, files=files, headers=headers,
                             auth=auth, verify=verify)
