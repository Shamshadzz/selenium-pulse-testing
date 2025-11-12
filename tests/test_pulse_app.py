import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TestPulseApp:
    
    def test_page_title(self, driver, base_url):
        """Test that the page title is correct"""
        driver.get(base_url)
        assert "Pulse App" in driver.title
    
    def test_element_present(self, driver, base_url):
        """Test that a specific element is present"""
        driver.get(base_url)
        page = BasePage(driver)
        
        # Example: Wait for React root element
        root_element = page.find_element((By.ID, "root"))
        assert root_element is not None
    
    def test_button_click(self, driver, base_url):
        """Test button click interaction"""
        driver.get(base_url)
        page = BasePage(driver)
        
        # Replace with your actual button selector
        button_locator = (By.CSS_SELECTOR, "button.your-button-class")
        page.click_element(button_locator)
        
        # Add assertions for expected behavior
        # Example: Check if some text appears after click
        # result_text = page.get_text((By.ID, "result"))
        # assert "Expected text" in result_text