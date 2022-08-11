import os
from framework.api.request import MakeRequest


class NexageAPIUtils:

    @staticmethod
    def setup():
        """Set Nexage API credentials/methods."""
        NexageAPIUtils.URL = "http://localhost:8080/api"
        NexageAPIUtils.GET_TOKEN = "/token/get"

    staticmethod
    def get_token(variant):
        url = NexageAPIUtils.URL + NexageAPIUtils.GET_TOKEN       
        data = {
                'variant': variant,               
                }               
        res = MakeRequest.post_binary_content(url=url, data=data)
        try:
            return res
        except KeyError:
            raise KeyError(f"Can't get a token through HTTP API: {res}")

        