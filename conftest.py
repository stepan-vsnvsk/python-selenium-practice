import pytest
import logging
from framework.ui.driver.singletone import Singletone
from framework.ui.driver.driver_utils.driver_util import DriverUtil
from framework.ui.driver.driver_utils.driver_util_waits import Waits
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


@pytest.fixture()
def test_dir_path():
    """Get 'test' directory path."""
    yield ConfigManager.get_value_from_config('test_dir')


@pytest.fixture(autouse=True)
def project_api_scheme_init(test_dir_path):
    """Set Union Reporting API scheme methods."""       
    api_scheme = JsonUtils.read_from_json(test_dir_path + 'api_data.json')
    UnionReportingAPIUtils.setup(api_scheme)
    yield


@pytest.fixture(autouse=True)
def read_regexp_file(test_dir_path):
    """Set regexp."""
    regexp_data = JsonUtils.read_from_json(test_dir_path + 'regex_data.json')
    UnionReportingRegexpUtils.setup(regexp_data)
    yield


@pytest.fixture(autouse=True)
def projects_id(test_dir_path):
    """Read project's id file."""
    projects_id = JsonUtils.read_from_json(test_dir_path + 'projects_id_data.json')
    yield projects_id


@pytest.fixture(autouse=True)
def test_data(test_dir_path):
    """Read common test data."""
    test_data = JsonUtils.read_from_json(test_dir_path + 'test_data.json')
    yield test_data


@pytest.fixture(autouse=True)
def log(request):
    """Logging initialization."""
    test_name = request.node.name
    Logger().set_file_handler(test_name)
    Logger.set_level(logging.INFO)
    yield
    Logger.remove_file_handler()
