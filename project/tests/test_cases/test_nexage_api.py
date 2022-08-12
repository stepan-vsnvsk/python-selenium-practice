from framework.ui.driver.driver_util import DriverUtil
from framework.util.config_manager import ConfigManager
from framework.util.logger import Logger as log
from project.api.nexage_api_utils import NexageAPIUtils
from project.pages.auth_form import AuthForm
from project.pages.projects_page import ProjectsPage
from project.pages.nexage_page import NexagePage
from framework.ui.driver.driver_util_waits import Waits
from selenium.webdriver.common.by import By
from framework.ui.base.elements.button_element import Button


class TestNexageAPI:    
    def test_case_get_tests_post_test(self):
        log.info("Test case 'Get Nexage tests / post test' is started")        
        
        log.info("Step #1: [API] Запросом к апи получить токен согласно номеру варианта.")
        variant = '2' #! hardcode
        token = NexageAPIUtils.get_token(variant)
        #str_token = token.decode("utf-8") #! not sure
        print(token) #! delete        
        assert token, \
            "Can't generate token " \
            "Expected result: token is generated."
        
        log.info("Step #2: [UI] Перейти на сайт. Пройти необходимую авторизацию."  
                 "С помощью cookie передать сгенерированный на шаге 1 токен."
                 "Обновить страницу.")
        url = ConfigManager.get_value_from_config('URL')
        DriverUtil.navigate_to(url)
        # auth_form = AuthForm()   #! need to implement     
        # auth_form.sign_in()        
        projects_page = ProjectsPage()
        projects_page.wait_until_page_will_appear()
        assert projects_page.is_page_open(), \
            "Can't open Projects page " \
            "Expected result: Projects page is open."
        
        cookie = {'name': 'token', 'value': str_token} #! do better
        
        DriverUtil.add_cookie(cookie)
        DriverUtil.refresh_page()        
        version = projects_page.get_portal_version()
        assert version == variant, \
            "Wrong version/variant number on footer" \
            f"Expected result: Version from page: {version} equals to token's variant {variant}"
        
        
        
        log.info("Step #3: [UI]/[API] Перейти на страницу проекта Nexage. "  
                 "Запросом к апи получить список тестов в JSON\XML-формате.")
         
        projects_page.click_nexage_projects_page()
        nexage_page = NexagePage()
        nexage_tests_ui = nexage_page.get_all_tests_data_per_page()        
        
        nexage_project_id = '1' #! hardcode
        nexage_tests_api = NexageAPIUtils.get_list_of_project_tests(nexage_project_id)

        # get list of start_time's from nexage_tests_ui #! ask about it
        start_times = [test.start_time for test in nexage_tests_ui]
        assert start_times == sorted(start_times, reverse=True), \
            "Test's aren't sorted in decreased by time order " \
            "Expected result: tests are sorted from recent to oldest. "
            f"Actual result: {start_times}"

        # compare all fields  do better!
        failed_to_compare = []
        for test_ui in nexage_tests_ui:
            test_api = next(
                (test_api for test_api in nexage_tests_api if test_ui.name == test_api.name), None)
            if test_ui != test_api:
                failed_to_compare.append(test_ui, test_api)
        assert not failed_to_compare, \
            "Tests from web UI page don't equals to tests from API response. " \
            "Expected result: all test's fields from IU and API equals. " \
            f"Actual result: from UI: {[x for x,y in failed_to_compare]} " \
            f"Actual result: from API:  {[y for x,y in failed_to_compare]}"     
        

        log.info("Step #4: [UI] Вернуться на предыдущую страницу в браузере (страница проектов)."
                 "Нажать на +Add. Ввести название проекта и сохранить."
                 "Для закрытия окна добавления проекта вызвать js-метод closePopUp()."
                 "Обновить страницу")
        DriverUtil.navigate_back()
        projects_page.click_add_project_button()
        projects_page.send_name_for_new_project()
        projects_page.click_submit_new_project_name()
        # JS close pop-up method
        DriverUtil.refresh_page()
        # Expectation:
        # После сохранения проекта появилось сообщение об успешном сохранении.
        # После вызова метода окно добавления проекта закрылось. 
        # После обновления страницы проект появился в списке
        


        

                 
         

        """
        no_such_thing = unique_element = Button(
            (By.XPATH, \
            "//a[contains(@href, 'useful_wait')]"),
            'whatever')
        Waits.wait_presence_of_element(no_such_thing)
        """

        