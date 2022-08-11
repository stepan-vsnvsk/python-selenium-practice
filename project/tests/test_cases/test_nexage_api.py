from framework.ui.driver.driver_util import DriverUtil
from framework.util.config_manager import ConfigManager
from framework.util.logger import Logger as log
from project.api.nexage_api_utils import NexageAPIUtils
from project.pages.auth_form import AuthForm
from project.pages.projects_page import ProjectsPage
from framework.ui.driver.driver_util_waits import Waits
from selenium.webdriver.common.by import By
from framework.ui.base.elements.button_element import Button


class TestNexageAPI:    
    def test_case_get_tests_post_test(self):
        log.info("Test case 'Get Nexage tests / post test' is started")        
        
        log.info("Step #1: [API] Запросом к апи получить токен согласно номеру варианта.")
        variant = '2' #! hardcode
        token = NexageAPIUtils.get_token(variant)
        str_token = token.decode("utf-8") #! not sure
        print(token) #! delete        
        assert token, \
            "Can't generate token " \
            "Expected result: token is generated."
        
        log.info("Step #2: [UI] Перейти на сайт. Пройти необходимую авторизацию."  
                 "С помощью cookie передать сгенерированный на шаге 1 токен (параметр token)."
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
        """
        no_such_thing = unique_element = Button(
            (By.XPATH, \
            "//a[contains(@href, 'free_man')]"),
            'whatever')
        Waits.wait_presence_of_element(no_such_thing)
        """
        version = projects_page.get_portal_version()
        assert version == variant, \
            "Wrong version/variant number on footer" \
            f"Expected result: Version from page: {version} equals to token's variant {variant}"



        