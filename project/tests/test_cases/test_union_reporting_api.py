from project.api.union_reporting_api_utils import UnionReportingAPIUtils
from project.pages.projects_page import ProjectsPage
from project.pages.all_tests_page import AllTestsPage
from project.pages.add_project_page import AddProjectPage
from project.models.test import TestModel
from framework.ui.driver.driver_utils.driver_util import DriverUtil
from framework.ui.driver.driver_utils.driver_util_window import DriverUtilWindow
from framework.api.request_utils import MakeRequestUtils
from framework.utils.logger import Logger as log
from framework.utils.str_utils import StrUtils
from framework.utils.json_utils import JsonUtils
from framework.utils.list_utils import ListUtil


class TestUnionReportingAPI:    
    def test_case_get_tests_add_new_project_post_new_test(self, test_data, basic_auth_url):
        log.info("Test case 'Get tests / Add new project / Post new test' is started.")
        log.info("Step #1: [API] Get a token (according to the variant) with HTTP API-querie.")
        variant = test_data['variant']        
        token = UnionReportingAPIUtils.get_token(variant).text                           
        assert token, \
            "Can't generate token " \
            "Expected result: token is generated."
        
        log.info("Step #2: [UI] Navigate to the site. Go through the authorisation. "  
                 "Pass generated token as a cookie. "
                 "Refresh the page.")        
        DriverUtil.navigate_to(basic_auth_url)               
        projects_page = ProjectsPage()
        projects_page.wait_until_page_will_appear()
        assert projects_page.is_page_open(), \
            "Can't open Projects page " \
            "Expected result: Projects page is opened."    
        
        token_key = test_data['cookie_key_token']        
        DriverUtil.add_cookie({token_key: token})
        DriverUtil.refresh_page()        
        version = projects_page.footer_form.get_portal_version()
        assert version == variant, \
            "Wrong version/variant number on footer " \
            "Expected result: Number on a footer equals to token's variant. " \
            f"Actual result: version from page: {version}, token's variant: {variant}"

        log.info("Step #3: [UI] Navigate to Nexage project page. "  
                 "[API] Get list of tests with API-querie in json.")
        project_name = test_data['testing_project_name']        
        project_id = projects_page.get_project_id_value_by_name(project_name)               
        projects_page.click_project_page_by_id(project_id)
        all_tests_page = AllTestsPage()
        all_tests_page.wait_until_page_will_appear()
        project_tests_ui = all_tests_page.get_all_tests_per_page()        
        project_tests_api = UnionReportingAPIUtils.get_list_of_project_tests(project_id)
        assert project_tests_api, \
            "Didn't get json-formatted data about project's tests through HTTP API. " \
            "Expected result: API method returns json-formatted list of project's tests"        
        start_times = [test.start_time for test in project_tests_ui]                
        assert ListUtil.check_order(start_times, reverse=True), \
            "Test's aren't sorted in decreasing by time order " \
            "Expected result: Tests' start times are sorted from recent to oldest. " \
            f"Actual result: {start_times}"

        failed_during_comparisons = []
        for test_ui in project_tests_ui:
            test_api = next((test_api for test_api in project_tests_api
                            if test_ui.name == test_api.name), None)
            if test_ui != test_api:
                failed_during_comparisons.append((test_ui, test_api))
        assert not failed_during_comparisons, \
            "Tests from web UI page don't equal to tests from API response. " \
            "Expected result: All test's fields from IU and API equal. " \
            f"Actual result: from UI: {[x() for x,y in failed_during_comparisons]} " \
            f"Actual result: from API:  {[y() for x,y in failed_during_comparisons]}"
        
        log.info("Step #4: [UI] Navigate back to previous page. "
                 "Click on +Add. Enter project's name and save. "
                 "Close the window. Refresh the page")
        DriverUtil.navigate_back()
        mock_test_obj = TestModel.generate_mock_object()  
        original_window_id = DriverUtilWindow.original_window_id()
        projects_page.click_add_project_button()
        add_project_page = AddProjectPage()
        DriverUtilWindow.switch_to_new_window(original_window_id)        
        add_project_page.send_name_for_new_project(mock_test_obj.project)
        add_project_page.click_submit_new_project_name()        
        assert add_project_page.is_message_new_project_saved_appeared(), \
            "New project wasn't saved " \
            "Expected result: Message about successful saving is shown"
        DriverUtilWindow.close_tab()        
        DriverUtilWindow.switch_to_original_window(original_window_id)             
        assert DriverUtilWindow.get_number_of_opened_windows() == 1, \
            "Page for adding new project is still opened" \
            "Expected result: 'Add new project' page is closed, there should be only one opened tab" \
            f"Actual result: opened tabs {opened_tabs}"
        assert not add_project_page.is_add_new_project_form_displayed(), \
            "Form for adding new project is still shown" \
            "Expected result: Add new project page is closed"

        total_projects_before = projects_page.get_number_of_projects()
        DriverUtil.refresh_page()
        total_projects_after = projects_page.get_number_of_projects()        
        newly_project_name_ui = projects_page.get_project_name_by_id(total_projects_after)
        assert total_projects_after == (total_projects_before + 1), \
            "New project is not added to the projects list. " \
            "Expected result: After refreshing page the new project should be in the list"        
        assert newly_project_name_ui == mock_test_obj.project, \
            "Newly project's name doesn't equal to a entered project's name " \
            "Expected result: Name from web-page is equal to a entered name through a form" \
            f"Actual result:  Web-page: {newly_project_name_ui}, entered one: {mock_test_obj.project}"

        log.info("Step #5: [UI] Navigate to the newly created project's page. "
                 "[API] Add test through HTTP API (with log and screenshot of a current page).")  
        projects_page.click_project_page_by_id(total_projects_after)
        UnionReportingAPIUtils.post_new_test(mock_test_obj)
        mock_test_obj.add_log(test_data['log_to_send_path'])
        log_response_code = UnionReportingAPIUtils.attach_log_to_test(mock_test_obj)
        screenshot_encoded = DriverUtil.get_screenshot_as_base64()
        mock_test_obj.attachment = screenshot_encoded       
        screenshot_response_code = UnionReportingAPIUtils.add_attachment_to_test(mock_test_obj)        
        assert MakeRequestUtils.check_status_code(log_response_code), \
               "Request for adding log to a test wasn't successful. " \
               "Expected result: Response code is in 'okay codes'"         
        assert MakeRequestUtils.check_status_code(screenshot_response_code), \
               "Request for adding screenshot to a test wasn't successful. " \
               "Expected result: Response code is in 'okay codes'"
        tests_page = AllTestsPage()            
        assert tests_page.wait_until_that_test_will_be_shown(mock_test_obj.test_id), \
            "Test is not shown. " \
            "Expected result: Test is shown on a project's all tests page. "
        