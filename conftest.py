import pytest
import logging
from framework.ui.driver.singletone import Singletone
from framework.ui.driver.driver_util import DriverUtil
from framework.ui.driver.driver_util_waits import Waits
from framework.util.logger import Logger
from framework.util.config_manager import ConfigManager
from project.api.nexage_api_utils import NexageAPIUtils

@pytest.fixture(autouse=True)
def driver_init():
    """Driver initialization.

    Setup: Call browser/driver.
    Teardown: Quit browser, clear Singletone.
    """
    DriverUtil()
    driver = DriverUtil.get_instance()    
    driver.maximize_window()
    yield
    DriverUtil.close_browser()
    Singletone.clear_singletone()


@pytest.fixture(autouse=True)
def waits_init(driver_init):
    """Set driver and timeout."""    
    Waits.setup()
    yield


@pytest.fixture(autouse=True)
def project_api_scheme_init():
    """Set VK API scheme methods."""    
    #api_data = JsonUtils.read_from_json(test_dir_path + 'test_api_data.json')
    NexageAPIUtils.setup()
    yield


@pytest.fixture(autouse=True)
def log(request):
    """Logging initialization."""
    test_name = request.node.name
    Logger().set_file_handler(test_name)
    Logger.set_level(logging.INFO)
    yield
    Logger.remove_file_handler()
