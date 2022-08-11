from framework.ui.driver.driver_util import DriverUtil
from framework.ui.driver.driver_util_waits import Waits
from framework.util.logger import Logger


class BaseForm:
    """
    Base class for Pages'/ Form's classes
    """   
    def is_page_open(self):
        """Check whether page is opened.

        Returns:
            True for success, False otherwise.
        """

        browser = DriverUtil.get_instance()
        Logger.info(f"Check if we on {self.__class__.__name__}")            
        elem_list = browser.find_elements(*self.unique_element.locator)
        return len(elem_list) > 0        

    def wait_until_page_will_appear(self):
        Waits.wait_presence_of_element(self.unique_element)
