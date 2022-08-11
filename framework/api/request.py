import requests


class MakeRequest:
    """Wrapper around requests lib."""

    @staticmethod
    def get(url, params={}, headers={}, auth=None, verify=False):
        """Make a HTTP API GET request.

        Note:
            No cares about exceptions.
        Returns:
            (tuple): Response dict or None.
        """

        response = requests.get(url, params=params, headers=headers, auth=auth, verify=verify)        
        return response.json()

    @staticmethod
    def get_binary_content(url, params={}, headers={}, auth=None, verify=False):
        """Make a HTTP API GET request.

        Returns:
            (bytes): response body as bytes.
        """

        response = requests.get(url, params=params, headers=headers, auth=auth, verify=verify)
        return response.content

    @staticmethod
    def post(url, data={}, params={}, headers={}, files=None, auth=None, verify=False):
        """Make a HTTP API POST request.

        Note:
            No cares about exceptions.
        Returns:
            Response dict or None.
        """

        response = requests.post(url, data=data, params=params, files=files, headers=headers, auth=auth, verify=verify)
        return response.json()


    @staticmethod
    def post_binary_content(url, data={}, params={}, headers={}, files=None, auth=None, verify=False):
        """Make a HTTP API POST request.

        Note:
            No cares about exceptions.
        Returns:
            (bytes): response body as bytes.
        """

        response = requests.post(url, data=data, params=params, files=files, headers=headers, auth=auth, verify=verify)
        return response.content