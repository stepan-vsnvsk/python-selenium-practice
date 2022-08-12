from selenium.webdriver.common.by import By
from framework.ui.base.base_form import BaseForm
from framework.ui.base.elements.text_element import Text
from project.util.str_util import StrProjectUtil
from project.models.test import TestModel

class NexagePage(BaseForm):
    def __init__(self):

        self.all_tests_per_page = Text(
            (By.XPATH, "//table[@class='table']"),
            'text from tests table')

    def get_all_tests_data_per_page(self):
        """
        Retrieve data about tests from page's table.
        Parse it by attributes.

        Returns:
                (TestModel objects): test's data.
        """

        tests_data = self.all_tests_per_page.get_text()
        list_of_str_tests = StrProjectUtil.parse_tests_data_from_projects_page(tests_data)
        tests_parsed_by_attr = StrProjectUtil.parse_tests_data_by_attributes(list_of_str_tests)
        return [TestModel(test_data) for test_data in tests_parsed_by_attr]