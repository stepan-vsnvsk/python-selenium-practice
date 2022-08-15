from framework.ui.driver.driver_utils.driver_util import DriverUtil
from framework.ui.driver.driver_utils.driver_util_window import DriverUtilWindow
from framework.utils.config_manager import ConfigManager
from framework.utils.logger import Logger as log
from project.api.union_reporting_api_utils import UnionReportingAPIUtils
from project.pages.projects_page import ProjectsPage
from project.pages.all_tests_page import AllTestsPage
from framework.ui.driver.driver_utils.driver_util_waits import Waits
from selenium.webdriver.common.by import By
from framework.ui.base.elements.button_element import Button
from framework.utils.str_utils import StrUtils
from project.models.test import TestModel


class TestNexageAPI:    
    def test_case_get_nexage_tests_add_new_project_post_new_test(self, test_data, projects_id):
        log.info("Test case 'Get Nexage tests / Add new project / Post new test is started.")        
        
        log.info("Step #1: [API] Запросом к апи получить токен согласно номеру варианта.")
        variant = test_data['variant']        
        token = UnionReportingAPIUtils.get_token(variant)                      
        assert token, \
            "Can't generate token " \
            "Expected result: token is generated."
        
        log.info("Step #2: [UI] Перейти на сайт. Пройти необходимую авторизацию. "  
                 "С помощью cookie передать сгенерированный на шаге 1 токен. "
                 "Обновить страницу.")
        url = ConfigManager.get_value_from_config('URL')
        DriverUtil.navigate_to(url)               
        projects_page = ProjectsPage()
        projects_page.wait_until_page_will_appear()
        assert projects_page.is_page_open(), \
            "Can't open Projects page " \
            "Expected result: Projects page is opened."        
        
        cookie = {'name': 'token', 'value': token} #! do better        
        DriverUtil.add_cookie(cookie)
        DriverUtil.refresh_page()        
        version = projects_page.get_portal_version()
        assert version == variant, \
            "Wrong version/variant number on footer " \
            f"Expected result: Version from page: {version} equals to token's variant {variant}"       
        
        
        log.info("Step #3: [UI] Перейти на страницу проекта Nexage. "  
                 "[API] Запросом к апи получить список тестов в JSON-XML-формате.")

        nexage_project_id = projects_id['Nexage'] 
        # envisia_project_id = projects_id['Envisia'] 
        projects_page.click_project_page_by_id(nexage_project_id)
        nexage_page = AllTestsPage()
        nexage_page.wait_until_page_will_appear()
        nexage_tests_ui = nexage_page.get_all_tests_data_per_page()

        nexage_tests_api = UnionReportingAPIUtils.get_list_of_project_tests(nexage_project_id)       

        start_times = [test.start_time for test in nexage_tests_ui]
        
        assert start_times == sorted(start_times, reverse=True), \
            "Test's aren't sorted in decreased by time order " \
            "Expected result: Tests are sorted from recent to oldest. " \
            f"Actual result: {start_times}"

        # compare all fields  do better!
        assert nexage_tests_ui
        assert nexage_tests_api, \
            "Decode Error occured"

        failed_during_comparisons = []
        for test_ui in nexage_tests_ui:
            test_api = next((test_api for test_api in nexage_tests_api \
                     if test_ui.name == test_api.name), None)
            print(f"UI: {test_ui}, API: {test_api}") #! delete it
            if test_ui != test_api:
                failed_during_comparisons.append((test_ui, test_api))
        assert not failed_during_comparisons, \
            "Tests from web UI page don't equal to tests from API response. " \
            "Expected result: All test's fields from IU and API equal. " \
            f"Actual result: from UI: {[x for x,y in failed_during_comparisons]} " \
            f"Actual result: from API:  {[y for x,y in failed_during_comparisons]}"     
        
        
        log.info("Step #4: [UI] Вернуться на предыдущую страницу в браузере. "
                 "Нажать на +Add. Ввести название проекта и сохранить. "
                 "Для закрытия окна добавления проекта вызвать js-метод closePopUp(). "
                 "Обновить страницу.")
        DriverUtil.navigate_back()

        # projects_page = ProjectsPage()

        mock_test_obj = TestModel.generate_mock_object()  
        original_window_id = DriverUtilWindow.original_window_id()       
         

        projects_page.click_add_project_button()
        DriverUtilWindow.switch_to_new_window(original_window_id)
        
        projects_page.send_name_for_new_project(mock_test_obj.project)
        projects_page.click_submit_new_project_name()
        new_project_saved = projects_page.is_message_new_project_saved_appeared()
        assert new_project_saved, \
            "New project doesn't saved " \
            "Expected result: Message about successful saving appeared"
        DriverUtilWindow.close_tab()        
        DriverUtilWindow.switch_to_original_window(original_window_id)    
                
        form_is_there = projects_page.is_add_new_project_form_appeared()
        assert not form_is_there, \
            "Form for adding new project is not closed " \
            "Expected result: After executing js-script the form is not displayed"
        
        total_projects_before = projects_page.get_number_of_projects()
        DriverUtil.refresh_page()
        total_projects_after = projects_page.get_number_of_projects()        
        newly_project_name_ui = projects_page.get_project_name_by_id(total_projects_after)
        assert total_projects_after == (total_projects_before + 1), \
            "New project is not added to the projects list. " \
            "Expected result: After refreshing page the new project should be in the list"        
        assert newly_project_name_ui == mock_test_obj.project, \
            "Newly project's name doesn't equal to a entered name " \
            "Expected result: Name from web-page is equal to a entered name through a form" \
            f"Actual result:  Web-page: {newly_project_name_ui}, entered one: {mock_test_obj.project}"



        
        log.info("Step #5: [UI] Перейти на страницу созданного проекта. "
                 "[API] Добавить тест через API(вместе с логом и скриншотом текущей страницы).")  
        projects_page.click_project_page_by_id(total_projects_after)
        test_id = UnionReportingAPIUtils.add_new_test(mock_test_obj)
        log_content = StrUtils.read_text(test_data['log_to_send_path'])        
        resp_log = UnionReportingAPIUtils.add_log_to_test(test_id, log_content)

        screenshot_encoded = DriverUtil.get_screenshot_as_base64() 
        # test_id, attachment, attachment_type='image/png'
        resp_attach = UnionReportingAPIUtils.add_attachment_to_test(test_id, screenshot_encoded)
        #print("resp_log: ", resp_log) 
        #print("resp_attach ", resp_attach)
        tests_page = AllTestsPage()

        tests_page.wait_until_that_test_will_be_shown(test_id)        
        
        #! same methods 
        test_is_there = tests_page.is_test_displayed(test_id)
        assert test_is_there, \
            "Test is not shown " \
            "Expected result: Test is shown on a project's all tests page"
                 
        
        
        """
        no_such_thing = unique_element = Button(
            (By.XPATH, \
            "//a[contains(@href, 'useful_wait')]"),
            'whatever')
        Waits.wait_presence_of_element(no_such_thing)
        """

        