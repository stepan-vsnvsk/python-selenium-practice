import os
import json 
from framework.api.request import MakeRequest
from project.models.test import Test 

class NexageAPIUtils:

    @staticmethod
    def setup():
        """Set Nexage API credentials/methods."""
        NexageAPIUtils.URL = "http://localhost:8080/api"
        NexageAPIUtils.GET_TOKEN = "/token/get"
        NexageAPIUtils.GET_PROJECT_TESTS_JSON = "/test/get/json"

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

    @staticmethod
    def get_list_of_project_tests(project_id):
        url = NexageAPIUtils.URL + NexageAPIUtils.GET_PROJECT_TESTS_JSON       
        data = {
                'projectId': str(project_id),               
                }
        response = MakeRequest.post_binary_content(url=url, data=data)
        tests_response = json.loads(response) #! move to separate method /requests or utils
        return [Test(test_data) for test_data in tests_response]
        

        