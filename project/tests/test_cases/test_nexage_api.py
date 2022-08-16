from project.api.union_reporting_api_utils import UnionReportingAPIUtils
from project.pages.projects_page import ProjectsPage
from project.pages.all_tests_page import AllTestsPage
from project.pages.add_project_page import AddProjectPage
from project.models.test import TestModel
from framework.ui.driver.driver_utils.driver_util import DriverUtil
from framework.ui.driver.driver_utils.driver_util_window import DriverUtilWindow
from framework.utils.config_manager import ConfigManager
from framework.utils.logger import Logger as log
from framework.utils.str_utils import StrUtils
from framework.utils.list_utils import ListUtil


class TestNexageAPI:    
    def test_case_get_nexage_tests_add_new_project_post_new_test(
                                    self, test_data, projects_id, basic_auth_url):
        log.info("Test case 'Get Nexage tests / Add new project / Post new test' is started.")
        log.info("Step #1: [API] Запросом к апи получить токен согласно номеру варианта.")
        variant = test_data['variant']        
        token = UnionReportingAPIUtils.get_token(variant)                      
        assert token, \
            "Can't generate token " \
            "Expected result: token is generated."
        
        log.info("Step #2: [UI] Перейти на сайт. Пройти необходимую авторизацию. "  
                 "С помощью cookie передать сгенерированный на шаге 1 токен. "
                 "Обновить страницу.")        
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

        log.info("Step #3: [UI] Перейти на страницу проекта Nexage. "  
                 "[API] Запросом к апи получить список тестов в JSON-XML-формате.")
        nexage_project_id = projects_id['Nexage']
        projects_page.click_project_page_by_id(nexage_project_id)
        nexage_page = AllTestsPage()
        nexage_page.wait_until_page_will_appear()
        nexage_tests_ui = nexage_page.get_all_tests_per_page()
        nexage_tests_api = UnionReportingAPIUtils.get_list_of_project_tests(nexage_project_id)       
        assert nexage_tests_api, \
            "Didn't get json-formatted data about project's tests through HTTP API. " \
            "Expected result: API method returns json-formatted list of project's tests"

        start_times = [test.start_time for test in nexage_tests_ui]
        is_start_times_sorted = ListUtil.check_order(start_times, reverse=True)        
        assert is_start_times_sorted, \
            "Test's aren't sorted in decreasing by time order " \
            "Expected result: Tests' start times are sorted from recent to oldest. " \
            f"Actual result: {start_times}"

        failed_during_comparisons = []
        for test_ui in nexage_tests_ui:
            test_api = next((test_api for test_api in nexage_tests_api
                            if test_ui.name == test_api.name), None)
            if test_ui != test_api:
                failed_during_comparisons.append((test_ui, test_api))
        assert not failed_during_comparisons, \
            "Tests from web UI page don't equal to tests from API response. " \
            "Expected result: All test's fields from IU and API equal. " \
            f"Actual result: from UI: {[x() for x,y in failed_during_comparisons]} " \
            f"Actual result: from API:  {[y() for x,y in failed_during_comparisons]}"
        
        log.info("Step #4: [UI] Вернуться на предыдущую страницу в браузере. "
                 "Нажать на +Add. Ввести название проекта и сохранить. "
                 "Для закрытия окна добавления проекта вызвать js-метод closePopUp(). "
                 "Обновить страницу.")
        DriverUtil.navigate_back()
        mock_test_obj = TestModel.generate_mock_object()  
        original_window_id = DriverUtilWindow.original_window_id()
        projects_page.click_add_project_button()
        add_project_page = AddProjectPage()
        DriverUtilWindow.switch_to_new_window(original_window_id)        
        add_project_page.send_name_for_new_project(mock_test_obj.project)
        add_project_page.click_submit_new_project_name()
        new_project_saved = add_project_page.is_message_new_project_saved_appeared()
        assert new_project_saved, \
            "New project wasn't saved " \
            "Expected result: Message about successful saving is shown"
        DriverUtilWindow.close_tab()        
        DriverUtilWindow.switch_to_original_window(original_window_id)
        opened_tabs = DriverUtilWindow.get_number_of_opened_windows()
        form_is_there = add_project_page.is_add_new_project_form_displayed()
        assert opened_tabs == 1, \
            "Page for adding new project is still opened" \
            "Expected result: 'Add new project' page is closed, there should be only one opened tab" \
            f"Actual result: opened tabs {opened_tabs}"
        assert not form_is_there, \
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

        log.info("Step #5: [UI] Перейти на страницу созданного проекта. "
                 "[API] Добавить тест через API (вместе с логом и скриншотом текущей страницы).")  
        projects_page.click_project_page_by_id(total_projects_after)
        test_id = UnionReportingAPIUtils.add_new_test(mock_test_obj)
        log_content = StrUtils.read_text(test_data['log_to_send_path'])        
        response_ok_log = UnionReportingAPIUtils.add_log_to_test(test_id, log_content)
        screenshot_encoded = DriverUtil.get_screenshot_as_base64()        
        response_ok_attach = UnionReportingAPIUtils.add_attachment_to_test(test_id, screenshot_encoded)        
        assert response_ok_log, \
            "Request for adding log to a test wasn't successful. " \
            "Expected result: Response code is in 'okay codes'"         
        assert response_ok_attach, \
            "Request for adding screenshot to a test wasn't successful. " \
            "Expected result: Response code is in 'okay codes'"
        tests_page = AllTestsPage()
        test_is_there = tests_page.wait_until_that_test_will_be_shown(test_id)        
        assert test_is_there, \
            "Test is not shown. " \
            "Expected result: Test is shown on a project's all tests page. "
