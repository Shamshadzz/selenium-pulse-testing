import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from config.test_data import TestData
import time

class TestPulseApp:
    
    def test_login_page_loads(self, driver, base_url):
        """Test that the login page loads correctly"""
        login_page = LoginPage(driver)
        login_page.navigate()
        
        # Verify title or key elements
        # Note: Title might be "AGEL | Project Lifecycle Platform" based on metadata
        assert "AGEL" in driver.title or "Pulse" in driver.title
        
        # Verify inputs are present
        assert login_page.is_element_present(LoginPage.USERNAME_INPUT)
        assert login_page.is_element_present(LoginPage.PASSWORD_INPUT)
    
    def test_failed_login(self, driver, base_url):
        """Test login with invalid credentials"""
        login_page = LoginPage(driver)
        login_page.navigate()
        
        # Use invalid credentials
        login_page.login("invalid@example.com", "WrongPass123")
        
        # Verify error indication
        # Based on inspection, the password field gets a red ring class 'ring-c_destructive.9'
        password_field = driver.find_element(*LoginPage.PASSWORD_INPUT)
        assert "ring-c_destructive.9" in password_field.get_attribute("class"), "Error styling not applied to password field"

    @pytest.mark.skip(reason="Need valid credentials to verify successful login")
    def test_successful_login(self, driver, base_url):
        """Test successful login flow"""
        login_page = LoginPage(driver)
        login_page.navigate()
        
        # Use credentials from TestData
        login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        
        # TODO: Add assertion for dashboard element once credentials are valid
        # Example: assert "Dashboard" in driver.title