from framework.ui.driver.browser_factory import BrowserFactory
from framework.ui.driver.singletone import Singletone
from framework.utils.logger import Logger


class DriverUtil(metaclass=Singletone):
    """Wrapper around Webdriver functionality."""

    _webdriver = None

    def __init__(self):
        """Initialization of Webdriver."""

        DriverUtil._webdriver = BrowserFactory.browser_initialization()

    @staticmethod
    def get_instance():
        """Global access point to Webdriver.

        Returns:
            Webdriver object or None
        """

        return DriverUtil._webdriver

    @staticmethod
    def close_browser():
        """Quit browser/driver."""
        DriverUtil._webdriver.quit()

    @staticmethod
    def navigate_to(url):
        """Open URL.

        Args:
            url(str): URL
        """

        Logger.info(f"Navigate to {url}")
        webdriver = DriverUtil.get_instance()
        webdriver.get(url)

    @staticmethod
    def refresh_page():
        """Reload a page."""
        Logger.info(f"Refresh a page")
        webdriver = DriverUtil.get_instance()
        webdriver.refresh()

    @staticmethod
    def add_cookie(cookie):
        """Add cookie to a browser context."""
        Logger.info(f"Add a cookie: {cookie}")
        webdriver = DriverUtil.get_instance()
        webdriver.add_cookie(cookie)

    @staticmethod
    def navigate_back():
        """Get back to previous page."""
        Logger.info(f"Navigate back to previous page.")
        webdriver = DriverUtil.get_instance()
        webdriver.back()

    @staticmethod
    def get_screenshot_as_base64():
        """Gets a screenshot of the current window as a base64 encoded string."""
        Logger.info("Make a current page screenshot as bas64-encoded string")
        webdriver = DriverUtil.get_instance()
        return webdriver.get_screenshot_as_base64()
