from selenium.webdriver.common.by import By
from framework.ui.base.base_form import BaseForm
from framework.ui.base.elements.button_element import Button
from framework.ui.base.elements.text_element import Text
from framework.ui.base.elements.text_field_element import TextField
from framework.ui.base.elements.form_element import Form
from framework.ui.base.elements.list_element import List
from project.utils.str_utils import UnionReportingStrUtils


class ProjectsPage(BaseForm):
    """Model of 'Projects' page."""

    def __init__(self):
    # out of init
    # implement driver init-on for BaseElement in conftest
        self.unique_element = Button(
                (By.XPATH, \
                "//a[contains(@href, 'allTests?projectId=1')]//parent::div[@class='list-group']"),
                'Unique element for the Projects page identity')

        self.add_project_button = Button(
                (By.XPATH, "//a[@href='addProject']"),
                'Add+ project button on the Projects page')
        
        self.all_projects_list = List(
                (By.XPATH, "//a[contains(@href, 'allTests?projectId')]"),
                'List of all projects on the Projects page')


        self.project_page_button_template = (
            (By.XPATH, "//a[contains(@href, 'projectId=%s')]"),
            "Button to project's tests page")
            

        #! not sure about proper place
        self.new_project_name_input = TextField(
                (By.XPATH, "//input[@name='projectName']"),
                "Input for new project's name form on the Projects page")
        self.new_project_name_submit_button = TextField(
                (By.XPATH, "//button[@type='submit']"),
                "Button for saving new project with a name on the Projects page")
        self.success_message_on_new_project_form = Text(
                (By.XPATH, "//form[@id='addProjectForm']//div[contains(@class, 'alert-success')]"),
                "Message about successful saving new project with a name")
        self.add_new_project_form = Form(
                (By.XPATH, "//form[@id='addProjectForm']"),
                "Form to add new project on the Projects page")

        
        
        #! move to base_page/footer form or something
        self.footer_version = Text(
                (By.XPATH, \
                "//footer//span"),
                'Portal version on footer')

    def get_portal_version(self):
        version = self.footer_version.get_text()
        return UnionReportingStrUtils.parse_portal_version_from_footer(version)
    
    def click_add_project_button(self):
        self.add_project_button.click()

    def send_name_for_new_project(self, project_name):
        self.new_project_name_input.send_word = project_name
        self.new_project_name_input.send_keys()

    def click_submit_new_project_name(self):
        self.new_project_name_submit_button.click()

    def is_message_new_project_saved_appeared(self):
        return self.success_message_on_new_project_form.is_displayed()

    def is_add_new_project_form_appeared(self):
        self.add_new_project_form.is_displayed()

    def get_number_of_projects(self):
        return len(self.all_projects_list.find_elements())

    def click_project_page_by_id(self, project_id):
        (loc_method, locator), name = self.project_page_button_template
        parametrized_locator = locator % project_id
        self.project_page_button = Button(
            (loc_method, parametrized_locator), name)        
        self.project_page_button.click()

    def get_project_name_by_id(self, project_id):
        (loc_method, locator), name = self.project_page_button_template
        parametrized_locator = locator % project_id
        self.project_page_button = Button(
            (loc_method, parametrized_locator), name)        
        return self.project_page_button.get_text()     


   
