from selenium.webdriver.common.by import By
from framework.ui.base.base_form import BaseForm
from framework.ui.base.elements.text_element import Text
from project.utils.str_utils import UnionReportingStrUtils


class FooterForm(BaseForm):
    """Model of the 'footer' form."""

    footer_version = Text((By.XPATH, "//footer//span"),
                          'Portal version on footer')

    def get_portal_version(self):
        """Portal version info according to a token."""
        version = self.footer_version.get_text()
        return UnionReportingStrUtils.parse_portal_version_from_footer(version)
