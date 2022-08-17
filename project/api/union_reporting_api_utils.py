from json.decoder import JSONDecodeError
from framework.api.request import MakeRequest
from project.models.test import TestModel 


class UnionReportingAPIUtils:
    """Functions to work with Union Reporting HTTP API."""

    @staticmethod
    def setup(api_data, api_endpoints):
        """Set Nexage API credentials/methods."""
        UnionReportingAPIUtils.BASE_URL = api_data['BASE_URL']
        UnionReportingAPIUtils.GET_TOKEN = api_endpoints['GET_TOKEN']
        UnionReportingAPIUtils.GET_PROJECT_TESTS_JSON = api_endpoints['GET_PROJECT_TESTS_JSON']
        UnionReportingAPIUtils.POST_NEW_TEST = api_endpoints['POST_NEW_TEST']
        UnionReportingAPIUtils.ADD_LOG_TO_TEST = api_endpoints['ADD_LOG_TO_TEST']
        UnionReportingAPIUtils.ADD_ATTACHMENT_TO_TEST = api_endpoints['ADD_ATTACHMENT_TO_TEST']

    @staticmethod
    def get_token(variant):
        url = UnionReportingAPIUtils.BASE_URL + UnionReportingAPIUtils.GET_TOKEN       
        data = {
                'variant': variant,               
                }
        return MakeRequest.post(url=url, data=data)
        
    @staticmethod
    def get_list_of_project_tests(project_id):
        """
        API method 'GET_PROJECT_TESTS_JSON' is unstable.
        It might return as a content xml or text instead of json.
        """

        url = UnionReportingAPIUtils.BASE_URL + UnionReportingAPIUtils.GET_PROJECT_TESTS_JSON       
        data = {
                'projectId': str(project_id),               
                }
        return MakeRequest.post(url=url, data=data)      
                 
    @staticmethod
    def post_new_test(testmodel_object):
        """
        Add a new test to a project's tests page.

        Args:
            (testmodel object): instance of TestModel class
        Returns:
            (int): Response's status code.
        """

        url = UnionReportingAPIUtils.BASE_URL + UnionReportingAPIUtils.POST_NEW_TEST       
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
        testmodel_object.test_id = response.text
        return response.status_code       

    @staticmethod
    def attach_log_to_test(testmodel_object, is_exception=False):
        url = UnionReportingAPIUtils.BASE_URL + UnionReportingAPIUtils.ADD_LOG_TO_TEST       
        data = {
                'testId': testmodel_object.test_id,
                'content': testmodel_object.log,
                'isException': is_exception                                         
                }        
        response = MakeRequest.post(url=url, data=data)               
        return response.status_code

    @staticmethod
    def add_attachment_to_test(testmodel_object, attachment_type='image/png'):
        url = UnionReportingAPIUtils.BASE_URL + UnionReportingAPIUtils.ADD_ATTACHMENT_TO_TEST       
        data = {
                'testId': testmodel_object.test_id,
                'content': testmodel_object.attachment,
                'contentType': attachment_type                                         
                }        
        response = MakeRequest.post(url=url, data=data)        
        return response.status_code
