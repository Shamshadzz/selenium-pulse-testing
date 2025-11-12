import pytest
from pages.login_page import LoginPage
from config.test_data import TestData

@pytest.mark.login
@pytest.mark.smoke
class TestLogin:
    
    def test_successful_login(self, driver, base_url):
        """Test successful login with valid credentials"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
    
    def test_invalid_login(self, driver, base_url):
        """Test login with invalid credentials"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(TestData.INVALID_USERNAME, TestData.INVALID_PASSWORD)
        
        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_message = login_page.get_error_message()
        assert len(error_message) > 0, "Error message is empty"
    
    def test_empty_credentials(self, driver, base_url):
        """Test login with empty credentials"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.click_login_button()
        
        # Verify validation or error
        assert login_page.is_error_displayed(), "No validation for empty fields"