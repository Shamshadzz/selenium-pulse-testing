from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from config.config import Config
import time


class LoginPage(BasePage):
    """Page Object Model for Login Page — robust version with onBlur triggers."""

    # Input fields
    USERNAME_INPUT = (By.ID, ":r1:")
    PASSWORD_INPUT = (By.ID, ":r2:")

    # Multiple locator options for the login button
    LOGIN_BUTTON_LOCATORS = [
        # Direct text (simplest)
        (By.XPATH, "//button[normalize-space(text())='Login']"),

        # Button containing nested text span
        (By.XPATH, "//button[normalize-space(.)='Login']"),

        # Fallback: a <span> with text 'Login' inside a button
        (By.XPATH, "//span[normalize-space(text())='Login']/ancestor::button"),
    ]

    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    LOADING_SPINNER = (By.CSS_SELECTOR, ".loading-spinner")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------
    def navigate(self):
        """Navigate to the login page and wait until input field is loaded."""
        self.driver.get(f"{Config.BASE_URL}/login")
        print(f"[DEBUG] Navigating to {Config.BASE_URL}/login")
        
        # Wait for the website to be fully loaded
        self.wait_for_page_load(timeout=10)

        try:
            self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
            print("[DEBUG] Login page loaded successfully.")
        except Exception:
            print("[WARN] Username input not found quickly — re-checking.")
            self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))

    # -----------------------------------------------------
    # INPUT HANDLING
    # -----------------------------------------------------
    def enter_username(self, username):
        """Enter username and blur field (trigger React onBlur validation)."""
        try:
            field = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
            field.clear()
            field.send_keys(username)
            field.send_keys(Keys.TAB) # Tab after filling input
            time.sleep(0.5) # Short wait after tab
            print(f"[DEBUG] Username entered: {username}")
        except Exception as e:
            print(f"[ERROR] Failed to enter username: {e}")
            raise

    def enter_password(self, password):
        """Enter password and blur field."""
        try:
            field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            field.clear()
            field.send_keys(password)
            field.send_keys(Keys.TAB) # Tab after filling input
            time.sleep(0.5) # Short wait after tab
            print("[DEBUG] Password entered and blurred")
        except Exception as e:
            print(f"[ERROR] Failed to enter password: {e}")
            raise

    # -----------------------------------------------------
    # LOGIN BUTTON HANDLING
    # -----------------------------------------------------
    def find_login_button(self):
        """Find login button using multiple fallback locator strategies."""
        print("\n[DEBUG] Searching for Login button...")

        for idx, locator in enumerate(self.LOGIN_BUTTON_LOCATORS, start=1):
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(locator)
                )
                print(f"✓ [FOUND] Login button located via strategy {idx}: {locator}")
                return element
            except Exception:
                print(f"✗ [MISS] Strategy {idx} failed: {locator}")

        self.driver.save_screenshot("login_error.png")
        print("[ERROR] Could not locate Login button. Screenshot saved as login_error.png")
        raise Exception("Login button not found with any of the tried locators.")

    def click_login_button(self):
        """Click the login button safely."""
        try:
            button = self.find_login_button()
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()
            print("[DEBUG] Login button clicked successfully.")
        except Exception as e:
            print(f"[ERROR] Click failed: {e}")
            self.driver.save_screenshot("login_click_error.png")
            print("[SCREENSHOT] Saved as login_click_error.png")
            raise

    # -----------------------------------------------------
    # FULL LOGIN FLOW
    # -----------------------------------------------------
    def login(self, username, password):
        """Perform full login: fill fields, blur, and submit."""
        print(f"\n[INFO] Starting login flow with username: {username}")
        initial_url = self.driver.current_url

        try:
            self.enter_username(username)
            self.enter_password(password)
            self.click_login_button()

            # Wait for page transition or dashboard load
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: d.current_url != initial_url
                )
                print("[DEBUG] URL changed after login — likely successful.")
            except Exception:
                print("[WARN] URL did not change (SPA app) — continuing anyway.")

            # Optional: wait for spinner to disappear
            if self.is_element_present(self.LOADING_SPINNER):
                try:
                    self.wait_for_element_to_disappear(self.LOADING_SPINNER, timeout=3)
                    print("[DEBUG] Loading spinner disappeared after login.")
                except Exception:
                    print("[WARN] Spinner did not disappear — continuing anyway.")

        except Exception as e:
            print(f"[ERROR] Login failed: {str(e)}")
            self.driver.save_screenshot("errors/login_failed.png")
            print("[SCREENSHOT] Saved as errors/login_failed.png")
            raise

    # -----------------------------------------------------
    # ERROR HANDLING
    # -----------------------------------------------------
    def get_error_message(self):
        """Return login error message text."""
        try:
            text = self.get_text(self.ERROR_MESSAGE)
            print(f"[DEBUG] Error message detected: {text}")
            return text
        except Exception:
            return ""

    def is_error_displayed(self):
        """Check if error message is visible."""
        visible = self.is_element_visible(self.ERROR_MESSAGE, timeout=5)
        print(f"[DEBUG] Error message visible: {visible}")
        return visible
