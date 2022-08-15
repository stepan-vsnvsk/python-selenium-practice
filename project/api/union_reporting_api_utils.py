import os
import json 
from json.decoder import JSONDecodeError
from framework.api.request import MakeRequest
from project.models.test import TestModel 

class UnionReportingAPIUtils:

    @staticmethod
    def setup(api_scheme):
        """Set Nexage API credentials/methods."""
        UnionReportingAPIUtils.URL = api_scheme['URL']
        UnionReportingAPIUtils.GET_TOKEN = api_scheme['GET_TOKEN']
        UnionReportingAPIUtils.GET_PROJECT_TESTS_JSON = api_scheme['GET_PROJECT_TESTS_JSON']
        UnionReportingAPIUtils.POST_NEW_TEST = api_scheme['POST_NEW_TEST']
        UnionReportingAPIUtils.ADD_LOG_TO_TEST = api_scheme['ADD_LOG_TO_TEST']
        UnionReportingAPIUtils.ADD_ATTACHMENT_TO_TEST = api_scheme['ADD_ATTACHMENT_TO_TEST']


    staticmethod
    def get_token(variant):
        url = UnionReportingAPIUtils.URL + UnionReportingAPIUtils.GET_TOKEN       
        data = {
                'variant': variant,               
                }               
        res = MakeRequest.post(url=url, data=data)
        return res.text
        
    @staticmethod
    def get_list_of_project_tests(project_id):
        url = UnionReportingAPIUtils.URL + UnionReportingAPIUtils.GET_PROJECT_TESTS_JSON       
        data = {
                'projectId': str(project_id),               
                }
        response = MakeRequest.post(url=url, data=data)
        print('STATUSCODE: ', response.status_code)
        print('HEADERS: ', (response.headers))
        print('CONTENT: ', response.text)
        try:
            return [TestModel(test_data) for test_data in response.json()]
        except JSONDecodeError:
             assert False

        # temp = response.text
        # tests_response = json.loads(temp) #! move to separate method /requests or utils      
        # return [TestModel(test_data) for test_data in tests_response]        

    @staticmethod
    def add_new_test(testmodel_object):
        """
        Add a new test to a project's tests page.

        Args:
            (testmodel object): instance of TestModel class
        Returns:
            (str): added test's id.
        """

        url = UnionReportingAPIUtils.URL + UnionReportingAPIUtils.POST_NEW_TEST       
        data = {
                'SID': testmodel_object.sid,
                'projectName': testmodel_object.project,
                'testName': testmodel_object.name,
                'methodName': testmodel_object.method,
                'env': testmodel_object.host,
                'start_time': testmodel_object.start_time if hasattr(testmodel_object, 'start_time') else '',                
                'browser': testmodel_object.browser if hasattr(testmodel_object, 'browser') else '' 
                }
        response = MakeRequest.post(url=url, data=data)
        return response.text 

    @staticmethod
    def add_log_to_test(test_id, log_file, is_exception=False):
        url = UnionReportingAPIUtils.URL + UnionReportingAPIUtils.ADD_LOG_TO_TEST       
        data = {
                'testId': test_id,
                'content': log_file,
                'isException': is_exception                                         
                }
        response = MakeRequest.post(url=url, data=data)
        return response.status_code 

    @staticmethod
    def add_attachment_to_test(test_id, attachment, attachment_type='image/png'):
        url = UnionReportingAPIUtils.URL + UnionReportingAPIUtils.ADD_ATTACHMENT_TO_TEST       
        data = {
                'testId': test_id,
                'content': attachment,
                'contentType': attachment_type                                         
                }
        response = MakeRequest.post(url=url, data=data)
        return response.status_code

    """
    if r.status_code == requests.codes.ok:
    """