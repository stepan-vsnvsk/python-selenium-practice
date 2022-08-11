from selenium.webdriver.common.by import By
from framework.ui.base.base_form import BaseForm
from framework.ui.base.elements.button_element import Button
from framework.ui.base.elements.text_element import Text
from project.util.str_util import StrProjectUtil


class ProjectsPage(BaseForm):
    """Model of 'Projects' page."""

    def __init__(self):
    # out of init
    # implement driver init-on for BaseElement in conftest
        self.unique_element = Button(
                (By.XPATH, \
                "//a[contains(@href, 'allTests?projectId=3')]//parent::div[@class='list-group']"),
                'unique element for page identity')
    
        #! move to base_page/footer form or something
        self.footer_version = Text(
                (By.XPATH, \
                "//footer//span"),
                'Portal version on footer')

    def get_portal_version(self):
        version = self.footer_version.get_text()
        return StrProjectUtil.parse_portal_version_from_footer(version)
    

   
