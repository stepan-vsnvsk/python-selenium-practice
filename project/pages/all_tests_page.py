from selenium.webdriver.common.by import By
from framework.ui.base.base_form import BaseForm
from framework.ui.base.elements.button_element import Button
from framework.ui.base.elements.text_element import Text
from framework.ui.driver.driver_utils.driver_util_waits import Waits
from project.utils.regexp_utils import UnionReportingRegexpUtils
from project.models.test import TestModel


class AllTestsPage(BaseForm):
    """Model of 'Tests' page (same page template for different projects)."""

    def __init__(self):
        self.unique_element = Text(
            (By.XPATH, "//a[contains(@href, 'testId')]"),
            'Unique element for the page identity')

        self.all_tests_per_page = Text(
            (By.XPATH, "//table[@class='table']"),
            'Text from tests table')

        self.test_by_id_template = (
            (By.XPATH, "//a[@href='testInfo?testId=%s']"),
            "Test by id button on 'all tests' page")

    def get_all_tests_data_per_page(self):
        """
        Retrieve data about tests from page's table.
        Parse it by attributes.

        Returns:
                (list) TestModel's objects.
        """

        tests_data = self.all_tests_per_page.get_text()
        list_of_str_tests = UnionReportingRegexpUtils.parse_tests_data_from_projects_page(tests_data)
        tests_parsed_by_attr = UnionReportingRegexpUtils.parse_tests_data_by_attributes(list_of_str_tests)
        return [TestModel(test_data) for test_data in tests_parsed_by_attr]

    def is_test_displayed(self, test_id):
        """
        Check whether test is shown on a page.

        Returns:
                (bool): True if shown, False otherwise.
        """

        (loc_method, locator), name = self.test_by_id_template
        parametrized_locator = locator % test_id
        self.test_by_id_button = Button(
            (loc_method, parametrized_locator), name)        
        return self.test_by_id_button.is_displayed()

    def wait_until_that_test_will_be_shown(self, test_id):
        """Wait for test to be shown on a project's tests page."""
        (loc_method, locator), name = self.test_by_id_template
        parametrized_locator = locator % test_id
        self.test_by_id_button = Button(
            (loc_method, parametrized_locator), name)
        Waits.wait_presence_of_element(self.test_by_id_button)
