from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from framework.utils.config_manager import ConfigManager


class BrowserFactory:
    BROWSERS = ['chrome']
    
    @staticmethod
    def browser_initialization():
        """Initialize proper driver/browser.

        Raises:
            Exception: if unknown browser in a config.
        """
        
        config_browser = ConfigManager.get_value_from_config('browser')
        if config_browser not in BrowserFactory.BROWSERS:
            raise Exception(f"Can't initialize {config_browser} driver")
        else:
            config_options, config_methods = ConfigManager.parse_config_for_driver()
            if config_browser == 'chrome':                
                options = webdriver.ChromeOptions()
                if config_options:
                    [options.add_argument(i) for i in config_options]
                return webdriver.Chrome(service=ChromeService(
                    ChromeDriverManager().install()), options=options)            
