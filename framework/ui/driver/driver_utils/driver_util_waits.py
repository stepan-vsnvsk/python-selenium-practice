from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from framework.ui.driver.driver_utils.driver_util import DriverUtil
from framework.utils.config_manager import ConfigManager
from framework.utils.logger import Logger


class Waits:
    """Wrapper around Webdriver 'Waits' functionality."""

    _driver = None
    timeout = None
    default_wait = ConfigManager.get_value_from_config("wait_timeout")
    browser = ConfigManager.get_value_from_config("browser")
    firefox_wait = ConfigManager.get_value_from_config("wait_timeout_firefox") 

    @staticmethod
    def setup():
        """Set driver and timeout."""

        Waits._driver = DriverUtil.get_instance()
        Waits.timeout = Waits.firefox_wait if Waits.browser == 'firefox' else Waits.default_wait

    @staticmethod
    def wait_presence_of_element(element):
        """Wait of a element presence and return it.

        Returns:
            WebElement object
        Raises:
          Timeout error: If the condition of a wait fails
        """

        Logger.info(f'Wait until {element.name} will be present in DOM')              
        return WebDriverWait(Waits._driver, timeout=Waits.timeout).until(
             EC.presence_of_element_located(element.locator))

    @staticmethod
    def wait_presence_of_all_elements(element):
        """Wait of a element(s) presence and return it.

        Returns:
            (list): WebElement objects
        Raises:
          Timeout error: If the condition of a wait fails
        """

        Logger.info(f'Wait until all {element.name} will be present in DOM')             
        return WebDriverWait(Waits._driver, timeout=Waits.timeout).until(
             EC.presence_of_all_elements_located(element.locator))

    @staticmethod
    def wait_until_clickable(element):
        """Wait for webelement to be clickable.

        Returns: Webelement object.

        Raises:
          Timeout error: If the condition of a wait fails.
        """

        Logger.info(f'Wait until {element.name} will be clickable')               
        return WebDriverWait(Waits._driver, timeout=Waits.timeout).until(
             EC.element_to_be_clickable(element.locator))    
    
    @staticmethod
    def wait_until_invisible(element):
        """Wait until element will disappear."""

        Logger.info(f'Wait until {element.name} will disappear')        
        WebDriverWait(Waits._driver, timeout=Waits.timeout).until(
            EC.invisibility_of_element_located(element.locator))

    @staticmethod
    def wait_visibility_of_element(element):
        """Wait until element will be visible."""
        
        Logger.info(f'Wait until {element.name} will be visible')
        WebDriverWait(Waits._driver, timeout=Waits.timeout).until(
            EC.visibility_of_element_located(element.locator))

    @staticmethod
    def wait_new_window():
        WebDriverWait(Waits._driver, timeout=Waits.timeout).until( 
            EC.number_of_windows_to_be(2))  
