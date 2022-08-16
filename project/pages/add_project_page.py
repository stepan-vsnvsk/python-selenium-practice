from selenium.webdriver.common.by import By
from framework.ui.base.base_form import BaseForm
from framework.ui.base.elements.text_element import Text
from framework.ui.base.elements.text_field_element import TextField
from framework.ui.base.elements.form_element import Form


class AddProjectPage(BaseForm):
    """Model of the 'Add a Project' page."""
    
    add_new_project_form = Form(
            (By.XPATH, "//form[@id='addProjectForm']"),
            "Form to add new project on the Projects page")
    new_project_name_input = TextField(
            (By.XPATH, "//input[@name='projectName']"),
            "Input for new project's name form on the Projects page")
    new_project_name_submit_button = TextField(
            (By.XPATH, "//button[@type='submit']"),
            "Button for saving new project with a name on the Projects page")
    success_message_on_new_project_form = Text(
            (By.XPATH, "//form[@id='addProjectForm']//div[contains(@class, 'alert-success')]"),
            "Message about successful saving new project with a name")

    def send_name_for_new_project(self, project_name):
        """
        Send project's name to a form.
        Pass that name as a element's property/attribute.
        """

        self.new_project_name_input.send_word = project_name
        self.new_project_name_input.send_keys()

    def click_submit_new_project_name(self):
        self.new_project_name_submit_button.click()

    def is_message_new_project_saved_appeared(self):
        return self.success_message_on_new_project_form.is_displayed()

    def is_add_new_project_form_displayed(self):
        self.add_new_project_form.is_displayed()
    