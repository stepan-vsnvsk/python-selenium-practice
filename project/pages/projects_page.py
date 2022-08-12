from selenium.webdriver.common.by import By
from framework.ui.base.base_form import BaseForm
from framework.ui.base.elements.button_element import Button
from framework.ui.base.elements.text_element import Text
from framework.ui.base.elements.text_field_element import TextField
from project.util.str_util import StrProjectUtil


class ProjectsPage(BaseForm):
    """Model of 'Projects' page."""

    def __init__(self):
    # out of init
    # implement driver init-on for BaseElement in conftest
        self.unique_element = Button(
                (By.XPATH, \
                "//a[contains(@href, 'allTests?projectId=3')]//parent::div[@class='list-group']"),
                'Unique element for page identity')
        self.nexage_projects_page_button = Button(
                (By.XPATH, "//a[contains(@href, 'projectId=1')]"),
                'Nexage projects page button')
        self.add_project_button = Button(
                (By.XPATH, "//button[@data-target='#addProject']"),
                'Add+ project button')

        #! not sure about proper place
        self.new_project_name_input = TextField(
                (By.XPATH, "//input[@name='projectName']"),
                "Input for new project's name")
        self.new_project_name_submit_button = TextField(
                (By.XPATH, "//button[@type='submit']"),
                "Button for saving new project with a name")
        
        
        #! move to base_page/footer form or something
        self.footer_version = Text(
                (By.XPATH, \
                "//footer//span"),
                'Portal version on footer')

    def get_portal_version(self):
        version = self.footer_version.get_text()
        return StrProjectUtil.parse_portal_version_from_footer(version)

    def click_nexage_projects_page(self):
        self.nexage_projects_page_button.click()

    def click_add_project_button(self):
        self.add_project_button.click()

    def send_name_for_new_project(self, project_name):
        self.new_project_name_input.send_word = project_name
        self.new_project_name_input.send_keys()

    def click_submit_new_project_name_(self):
        self.new_project_name_submit_button.click()
    

   
