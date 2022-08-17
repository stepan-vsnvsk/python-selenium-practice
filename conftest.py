import os
import pytest
import logging
from framework.ui.driver.singletone import Singletone
from framework.ui.driver.driver_utils.driver_util import DriverUtil
from framework.ui.driver.driver_utils.driver_util_waits import Waits
from framework.ui.base.elements.base_element import BaseElement
from framework.utils.config_manager import ConfigManager
from framework.utils.logger import Logger
from framework.utils.json_utils import JsonUtils
from project.api.union_reporting_api_utils import UnionReportingAPIUtils
from project.utils.regexp_utils import UnionReportingRegexpUtils


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
def base_element_init(driver_init):
    """Set driver."""
    BaseElement.setup()
    yield


@pytest.fixture(scope='session')
def test_dir_path():
    """Get 'test' directory path."""
    yield ConfigManager.get_value_from_config('test_dir')


@pytest.fixture(scope='session', autouse=True)
def project_api_scheme_init(test_dir_path):
    """Set Union Reporting API scheme methods."""       
    api_data = JsonUtils.read_from_json(test_dir_path + 'api_data.json')
    api_endpoints = JsonUtils.read_from_json(test_dir_path + 'api_endpoints.json')
    UnionReportingAPIUtils.setup(api_data, api_endpoints)
    yield


@pytest.fixture(scope='session', autouse=True)
def read_regexp_file(test_dir_path):
    """Set regexp."""
    regexp_data = JsonUtils.read_from_json(test_dir_path + 'regex_data.json')
    UnionReportingRegexpUtils.setup(regexp_data)
    yield


@pytest.fixture(scope='session')
def test_data(test_dir_path):
    """Read common test data."""
    test_data = JsonUtils.read_from_json(test_dir_path + 'test_data.json')
    yield test_data


@pytest.fixture()
def basic_auth_url():
    """Pass user's credentials through URL."""    
    username = os.environ['username']
    secret = os.environ['password']
    url = ConfigManager.get_value_from_config('URL')
    find_by = '//'
    index = url.find(find_by) + len(find_by)    
    yield f"{url[:index]}{username}:{secret}@{url[index:]}"


@pytest.fixture(autouse=True)
def log(request):
    """Logging initialization."""
    test_name = request.node.name
    Logger().set_file_handler(test_name)
    Logger.set_level(logging.INFO)
    yield
    Logger.remove_file_handler()
