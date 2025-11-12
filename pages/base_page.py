from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.config import Config

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text
    
    def wait_for_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def is_element_present(self, locator):
        """Return True if at least one element matching locator exists in the DOM."""
        try:
            elements = self.driver.find_elements(*locator)
            return len(elements) > 0
        except Exception:
            return False

    def is_element_visible(self, locator, timeout=10):
        """Return True if element becomes visible within timeout, False otherwise."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait until an element is no longer visible/present.

        Returns True when the element is gone or not visible. Raises on timeout.
        """
        t = timeout if timeout is not None else Config.EXPLICIT_WAIT
        return WebDriverWait(self.driver, t).until(EC.invisibility_of_element_located(locator))

    def wait_for_page_load(self, timeout=None):
        """Wait for page to finish loading by waiting for document.readyState === 'complete'."""
        t = timeout if timeout is not None else Config.EXPLICIT_WAIT
        WebDriverWait(self.driver, t).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    def select_dropdown_by_visible_text(self, locator, text):
        """Select an option from dropdown by visible text."""
        from selenium.webdriver.support.ui import Select
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to become visible."""
        t = timeout if timeout is not None else Config.EXPLICIT_WAIT
        return self.wait.until(EC.visibility_of_element_located(locator))