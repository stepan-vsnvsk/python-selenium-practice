from selenium.webdriver.common.by import By
from framework.ui.base.base_form import BaseForm
from framework.ui.base.elements.button_element import Button
from framework.ui.base.elements.list_element import List
from project.pages.footer_form import FooterForm


class ProjectsPage(BaseForm):
    """Model of the 'Projects' page."""

    footer_form = FooterForm()

    unique_element = Button(
                (By.XPATH,
                 "//a[contains(@href, 'allTests?projectId=1')]//parent::div[@class='list-group']"),
                'Unique element for the Projects page identity')
    add_project_button = Button((By.XPATH, "//a[@href='addProject']"),
                                'Add+ project button on the Projects page')
    all_projects_list = List((By.XPATH, "//a[contains(@href, 'allTests?projectId')]"),
                             'List of all projects on the Projects page')

    def __init__(self):
        self.project_page_button_template = (
            (By.XPATH, "//a[@href='allTests?projectId=%s']"),
            "Button to project's tests page")     
    
    def click_add_project_button(self):
        self.add_project_button.click()    

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
