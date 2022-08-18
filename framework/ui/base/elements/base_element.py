from selenium.common.exceptions import NoSuchElementException
from framework.ui.driver.driver_utils.driver_util import DriverUtil
from framework.ui.driver.driver_utils.driver_util_waits import Waits
from framework.utils.config_manager import ConfigManager
from framework.utils.logger import Logger


class BaseElement:
    """
    Base class for all Element's classes
    """
    browser = None

    def __init__(self, loc, name_elem):
        self.locator = loc
        self.name = name_elem

    @staticmethod
    def setup():
        """Set driver."""
        BaseElement.browser = DriverUtil.get_instance()                       

    def find_element(self):
        """Wait of element presence and find webelement.

        Returns:
            WebElement object
        Raises:
          Timeout error: If the condition of a wait fails
        """

        Logger.info(f"Find {self.name}")
        return Waits.wait_presence_of_element(self)

    def find_elements(self):
        """Wait of elements presence and find webelements.

        Returns:
            WebElement objects (list)
        Raises:
          Timeout error: If the condition of a wait fails
        """

        Logger.info(f"Find {self.name} elements")
        return Waits.wait_presence_of_all_elements(self)
        
    def is_displayed(self):
        """Check whether a element is displayed on a page.

        Returns:
            True for success, False otherwise.
        """ 

        Logger.info(f"Check if {self.name} is displayed")        
        try:
            return self.browser.find_element(*self.locator).is_displayed()
        except NoSuchElementException:
            Logger.info(f"Can't find {self.name}")        
            return False

    def click(self):
        """Perform click action on a element."""
        
        Logger.info(f"Click {self.name}")
        return Waits.wait_until_clickable(self).click()
        
    def get_text(self):
        """Find element and get text.

        Returns:
            Text (str) from element.
        """
        
        Logger.info(f"Get text from {self.name}")
        Waits.wait_presence_of_element(self)
        return self.browser.find_element(*self.locator).text

    def get_attribute_value(self, attr):
        """Find element and get attribute value

        Args:
            attr(str): attribute's name of element which value we want to get
        Returns:
            Element's attribute value (str).
        """
        element = self.find_element()
        Logger.info(f"Get {attr} from {self.name}")
        return element.get_attribute(attr)
