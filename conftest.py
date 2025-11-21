import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config
from pages.login_page import LoginPage
from config.test_data import TestData
import time

def _create_driver():
    """Helper function to create a Chrome driver with standard options."""
    chrome_options = Options()
    # Note: Running in visible mode (not headless) - browser window will be visible
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Allow camera and geolocation permissions automatically
    chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Auto-allow camera/mic
    chrome_options.add_argument("--use-fake-device-for-media-stream")  # Use fake camera device
    
    # Set preferences for automatic permissions
    prefs = {
        "profile.default_content_setting_values.media_stream_camera": 1,  # Allow camera
        "profile.default_content_setting_values.media_stream_mic": 1,     # Allow microphone
        "profile.default_content_setting_values.geolocation": 1,          # Allow geolocation
        "profile.default_content_setting_values.notifications": 1         # Allow notifications
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Install chromedriver and get the correct path
    driver_path = ChromeDriverManager().install()
    # Fix for webdriver-manager returning THIRD_PARTY_NOTICES path
    if "THIRD_PARTY_NOTICES" in driver_path:
        import os
        driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")
    
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()
    return driver

def _login_as_role(driver, role):
    """Helper function to login with a specific role."""
    credentials = TestData.get_credentials(role)
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(credentials["username"], credentials["password"])
    # Wait for URL to change or specific post-login element instead of fixed sleep
    # This is faster than a fixed sleep
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        # Wait for URL to change from /login (max 5 seconds)
        WebDriverWait(driver, 5).until(
            lambda d: "/login" not in d.current_url.lower()
        )
    except Exception:
        # If URL doesn't change, just proceed - login might be successful anyway
        pass

@pytest.fixture(scope="function")
def driver():
    """Setup and teardown for Chrome driver (function scope)"""
    driver = _create_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def logged_in_driver():
    """Setup a logged-in driver with contractor role (backward compatibility)"""
    driver = _create_driver()
    _login_as_role(driver, "contractor")
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def contractor_driver():
    """Setup a logged-in driver with contractor role - persists across tests"""
    driver = _create_driver()
    _login_as_role(driver, "contractor")
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def admin_driver():
    """Setup a logged-in driver with admin role - persists across tests"""
    driver = _create_driver()
    _login_as_role(driver, "admin")
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def project_manager_driver():
    """Setup a logged-in driver with project manager role - persists across tests"""
    driver = _create_driver()
    _login_as_role(driver, "project_manager")
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def client_driver():
    """Setup a logged-in driver with client role - persists across tests"""
    driver = _create_driver()
    _login_as_role(driver, "client")
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def contractor_incharge_driver():
    """Setup a logged-in driver with contractor incharge role - persists across tests"""
    driver = _create_driver()
    _login_as_role(driver, "contractor_incharge")
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def block_engineer_driver():
    """Setup a logged-in driver with block engineer role - persists across tests"""
    driver = _create_driver()
    _login_as_role(driver, "block_engineer")
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def quality_inspector_driver():
    """Setup a logged-in driver with quality inspector role - persists across tests"""
    driver = _create_driver()
    _login_as_role(driver, "quality_inspector")
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    return Config.BASE_URL