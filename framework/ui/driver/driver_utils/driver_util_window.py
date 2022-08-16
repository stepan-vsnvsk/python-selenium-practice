from framework.ui.driver.driver_utils.driver_util import DriverUtil
from framework.ui.driver.driver_utils.driver_util_waits import Waits
from framework.utils.logger import Logger


class DriverUtilWindow:
    """Webdriver's functionality for windows/tabs handling."""

    @staticmethod
    def original_window_id():
        """Get current window id.

        Returns:
            window's ID (str)
        """

        Logger.info("Save current window id")
        webdriver = DriverUtil.get_instance() 
        return webdriver.current_window_handle

    @staticmethod
    def switch_to_new_window(original_window):
        """Switch to a new window.

        Iterate over open windows and go not to a current one.
        """

        Logger.info("Switch to a New Tab")
        webdriver = DriverUtil.get_instance()
        Waits.wait_new_window()   
        
        for window_handle in webdriver.window_handles:
            if window_handle != original_window:
                webdriver.switch_to.window(window_handle)
                break

    @staticmethod
    def close_tab():
        """Close current tab."""
        Logger.info("Close current tab")
        webdriver = DriverUtil.get_instance()
        webdriver.close()

    @staticmethod
    def switch_to_original_window(window_id):
        """Switch to window with that ID.

        Args:
            window_id(str): previously saved window's ID
        """

        Logger.info(f"Switch to original window {window_id}")
        webdriver = DriverUtil.get_instance()
        webdriver.switch_to.window(window_id) 

    @staticmethod
    def get_number_of_opened_windows():
        """Check how many windows/tabs is opened already."""
        Logger.info(f"Check number of opened windows/tabs")
        webdriver = DriverUtil.get_instance()
        return len(webdriver.window_handles)
