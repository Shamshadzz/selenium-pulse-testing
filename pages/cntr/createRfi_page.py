from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from pages.base_page import BasePage
from config.config import Config
import time


class CreateRfiPage(BasePage):
    """Ultra-fast, stable Create RFI Page with zero manual pauses."""

    CREATE_RFI_BUTTON = (By.XPATH, "//button[normalize-space()='Create RFI']")
    FORM_CONTAINER = (By.CSS_SELECTOR, ".steps__content.h_full.ov_auto")

    # Dropdown triggers
    PLOT_TRIGGER = (By.XPATH, "//label[.//span[normalize-space()='Plot No. *']]/following-sibling::div//button[@data-part='trigger']")
    BLOCK_TRIGGER = (By.XPATH, "//label[.//span[normalize-space()='Block No. *']]/following-sibling::div//button[@data-part='trigger']")
    PACKAGE_TRIGGER = (By.XPATH, "//label[.//span[normalize-space()='Package *']]/following-sibling::div//button[@data-part='trigger']")
    SUBPACKAGE_TRIGGER = (By.XPATH, "//label[.//span[normalize-space()='Sub-Package *']]/following-sibling::div//button[@data-part='trigger']")
    ACTIVITY_TRIGGER = (By.XPATH, "//label[.//span[normalize-space()='Activity *']]/following-sibling::div//button[@data-part='trigger']")
    SUBACTIVITY_TRIGGER = (By.XPATH, "//label[.//span[normalize-space()='Sub-Activity *']]/following-sibling::div//button[@data-part='trigger']")
    UNIT_TRIGGER = (By.XPATH, "//label[.//span[contains(., 'Unit of Measurement')]]/following-sibling::div//button[@data-part='trigger']")
    INSPECTION_CHECKPOINT_TRIGGER = (By.XPATH, "//label[.//span[contains(., 'Inspection Checkpoint')]]/following-sibling::div//button[@data-part='trigger']")
    INSPECTION_CHECKLIST_TRIGGER = (By.XPATH, "//label[.//span[contains(., 'Inspection Checklist')]]/following-sibling::div//button[@data-part='trigger']")

    # Inputs
    LOCATION_INPUT = (By.XPATH, "//label[span[normalize-space()='Location *']]/following::input[@placeholder='Select Location'][1]")
    QUANTITY_INPUT = (By.XPATH, "//input[@placeholder='Enter Quantity']")
    SUBCONTRACTOR_INPUT = (By.XPATH, "//input[@placeholder='Enter sub contractor name']")

    # Buttons
    PROCEED_BUTTON = (By.XPATH, "//button[normalize-space()='Proceed']")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")
    SUCCESS_TOAST = (By.XPATH, "//*[contains(text(),'successfully') or contains(text(),'Success')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)  # Increased to 10 seconds

    # ---------- helpers ----------

    def scroll_into_view(self, el):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass

    def safe_click(self, locator):
        """Click element only when clickable."""
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self.scroll_into_view(el)
        self.driver.execute_script("arguments[0].click();", el)
        return el

    def safe_input(self, locator, text):
        """Type text and confirm persistence instantly."""
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self.scroll_into_view(el)
        el.clear()
        el.send_keys(text)
        el.send_keys(Keys.TAB)
        self.wait.until(lambda d: text.lower() in (el.get_attribute("value") or "").lower())
        print(f"[INPUT] {text} -> {locator}")
        return el

    def wait_for_field_ready(self, locator, field_name, timeout=2):
        """Wait until field becomes visible & enabled."""
        self.wait.until(lambda d: d.find_element(*locator).is_enabled())
        print(f"[READY] {field_name}")
        return True

    # ---------- dropdown logic ----------

    def select_dropdown_with_dependency_wait(
        self, trigger_locator, option_text, dependent_field_locator=None,
        dependent_field_name=None, is_multiselect=False
    ):
        """Select one or multiple dropdown options with zero manual pauses."""
        options = option_text if isinstance(option_text, list) else [option_text]
        print(f"[SELECT] {options}")

        try:
            # Open dropdown
            print(f"[DEBUG] Clicking dropdown trigger: {trigger_locator}")
            trigger = self.safe_click(trigger_locator)
            dropdown_open = (By.XPATH, "//div[@data-part='content' and @data-state='open']")
            self.wait.until(EC.presence_of_element_located(dropdown_open))
            print("[DEBUG] Dropdown opened successfully")
            
            # Wait for options to load (important for API-driven dropdowns)
            time.sleep(1.0)  # Give time for options to load from API
            
            # Debug: Show available options
            try:
                all_options = self.driver.find_elements(By.XPATH, "//div[@data-part='content']//span")
                available_options = [opt.text for opt in all_options if opt.text.strip()]
                print(f"[DEBUG] Available options ({len(available_options)}): {available_options[:5]}...")  # Show first 5
                
                if not available_options:
                    print("[WARNING] No options found in dropdown! Waiting longer...")
                    time.sleep(2.0)  # Wait more for data to load
                    all_options = self.driver.find_elements(By.XPATH, "//div[@data-part='content']//span")
                    available_options = [opt.text for opt in all_options if opt.text.strip()]
                    print(f"[DEBUG] After waiting: Available options ({len(available_options)}): {available_options[:5]}...")
                    
                    if not available_options:
                        print("[ERROR] Still no options available!")
                        self.driver.save_screenshot("no_dropdown_options.png")
                        print("[DEBUG] Screenshot saved as no_dropdown_options.png")
            except Exception as e:
                print(f"[WARNING] Could not list dropdown options: {e}")
                
        except TimeoutException as e:
            print(f"[ERROR] Failed to open dropdown: {str(e)}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot("errors/dropdown_open_failed.png")
                print("[DEBUG] Screenshot saved as errors/dropdown_open_failed.png")
            except:
                pass
            raise

        # Select each option
        for opt_text in options:
            try:
                opt_xpath = f"//div[@data-part='content']//span[normalize-space()='{opt_text}']"
                print(f"[DEBUG] Looking for option: '{opt_text}'")
                option = self.wait.until(EC.element_to_be_clickable((By.XPATH, opt_xpath)))
                self.scroll_into_view(option)
                self.driver.execute_script("arguments[0].click();", option)
                print(f"[SUCCESS] Selected '{opt_text}'")
            except TimeoutException:
                print(f"[ERROR] Could not find option '{opt_text}' in dropdown")
                raise

        # Close dropdown
        if is_multiselect:
            # click outside to persist selection
            self.driver.execute_script("document.body.click();")
            print("[DEBUG] Closed multi-select dropdown.")
            try:
                first_val = options[0]
                self.wait.until(lambda d: first_val.lower() in (d.find_element(*trigger_locator).get_attribute("value") or "").lower())
            except Exception:
                print("[WARN] Could not confirm persistence.")
        else:
            try:
                option.send_keys(Keys.TAB)
            except Exception:
                self.driver.execute_script("document.body.click();")

        # Wait for dropdown to close before moving on
        try:
            self.wait.until(EC.invisibility_of_element_located(dropdown_open))
        except TimeoutException:
            print("[WARN] Dropdown did not close completely.")

        # Handle dependent field
        if dependent_field_locator and dependent_field_name:
            self.wait_for_field_ready(dependent_field_locator, dependent_field_name)

    # ---------- actions ----------

    def navigate(self):
        print(f"[DEBUG] Navigating to {Config.BASE_URL}/welcome")
        self.driver.get(f"{Config.BASE_URL}/welcome")
        self.wait_for_page_load()
    
    def debug_page_state(self):
        """Debug helper to check current page state."""
        print("\n=== DEBUG: PAGE STATE ===")
        try:
            print(f"Current URL: {self.driver.current_url}")
            
            # Check if Create RFI button exists
            create_rfi_buttons = self.driver.find_elements(*self.CREATE_RFI_BUTTON)
            print(f"Create RFI buttons found: {len(create_rfi_buttons)}")
            
            # Check if form is open
            form_containers = self.driver.find_elements(*self.FORM_CONTAINER)
            print(f"Form containers found: {len(form_containers)}")
            
            if form_containers:
                # Check if Plot dropdown exists
                plot_triggers = self.driver.find_elements(*self.PLOT_TRIGGER)
                print(f"Plot No. dropdowns found: {len(plot_triggers)}")
                if plot_triggers:
                    print(f"  Plot dropdown visible: {plot_triggers[0].is_displayed()}")
                    print(f"  Plot dropdown enabled: {plot_triggers[0].is_enabled()}")
        except Exception as e:
            print(f"Error in debug: {e}")
        print("=== END DEBUG ===\n")

    def open_form(self):
        print("[INFO] Opening Create RFI form...")
        try:
            # Wait for Create RFI button to be visible and clickable
            create_rfi_btn = self.wait.until(EC.element_to_be_clickable(self.CREATE_RFI_BUTTON))
            self.scroll_into_view(create_rfi_btn)
            time.sleep(0.5)  # Small wait for page to stabilize
            create_rfi_btn.click()
            
            # Wait for form to open
            self.wait.until(EC.visibility_of_element_located(self.FORM_CONTAINER))
            print("[INFO] Form container visible, waiting for data to load...")
            
            # Wait longer for API data to load (dropdown options need to fetch from backend)
            time.sleep(2.0)  # Increased wait for API data
            print("[SUCCESS] Form opened and data should be loaded.")
        except Exception as e:
            print(f"[ERROR] Failed to open form: {str(e)}")
            raise

    def fill_form(self):
        print("=== START FORM FILL ===")
        
        # Debug page state
        self.debug_page_state()
        
        # Wait for first field to be ready
        try:
            print("[INFO] Waiting for Plot No. field to be ready...")
            self.wait.until(EC.element_to_be_clickable(self.PLOT_TRIGGER))
            time.sleep(0.5)  # Additional stabilization time
            print("[SUCCESS] Form is ready for input.")
        except Exception as e:
            print(f"[ERROR] Form fields not ready: {str(e)}")
            # Take screenshot
            try:
                self.driver.save_screenshot("form_not_ready.png")
                print("[DEBUG] Screenshot saved as form_not_ready.png")
            except:
                pass
            raise
        
        self.select_dropdown_with_dependency_wait(self.PLOT_TRIGGER, "S05b", self.BLOCK_TRIGGER, "Block No.")
        self.select_dropdown_with_dependency_wait(self.BLOCK_TRIGGER, "BL05", self.PACKAGE_TRIGGER, "Package")
        self.select_dropdown_with_dependency_wait(self.PACKAGE_TRIGGER, "Civil", self.SUBPACKAGE_TRIGGER, "Sub-Package")
        self.select_dropdown_with_dependency_wait(self.SUBPACKAGE_TRIGGER, "MMS Installation", self.ACTIVITY_TRIGGER, "Activity")
        self.select_dropdown_with_dependency_wait(self.ACTIVITY_TRIGGER, "MMS Installation", self.SUBACTIVITY_TRIGGER, "Sub-Activity")
        self.select_dropdown_with_dependency_wait(self.SUBACTIVITY_TRIGGER, "MMS Installation", self.LOCATION_INPUT, "Location")

        # Multi-select Location
        self.select_dropdown_with_dependency_wait(self.LOCATION_INPUT, ["R01-T01", "R01-T02"], self.QUANTITY_INPUT, "Quantity", is_multiselect=True)

        self.safe_input(self.QUANTITY_INPUT, "25")
        self.select_dropdown_with_dependency_wait(self.UNIT_TRIGGER, "MTR")
        self.safe_input(self.SUBCONTRACTOR_INPUT, "TechBuild Contractors Pvt Ltd")

        self.select_dropdown_with_dependency_wait(
            self.INSPECTION_CHECKPOINT_TRIGGER,
            "If Tracker: Tracker Alignment, Tightening & Torquing up to Torque Tube incl. Transmission Shaft If Fixed Tilt: Fixed Tilt Alignment, Tightening & Torquing up to bracing, perlin and all asembly parts",
            self.INSPECTION_CHECKLIST_TRIGGER,
            "Inspection Checklist"
        )
        self.select_dropdown_with_dependency_wait(
            self.INSPECTION_CHECKLIST_TRIGGER,
            "PV Module Mounting Structure Installation Protocol - Tracker"
        )
        print("=== FORM FILL COMPLETE ===")

    def submit_form(self):
        """Click Proceed button to move from Step 1 (RFI details) to Step 2 (Inspection Checklist)."""
        print("[ACTION] Clicking Proceed to go to Inspection Checklist...")
        try:
            # Wait for Proceed button and click it
            proceed_btn = self.wait.until(EC.element_to_be_clickable(self.PROCEED_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", proceed_btn)
            self.driver.execute_script("arguments[0].click();", proceed_btn)
            print("[SUCCESS] Clicked Proceed - navigating to Inspection Checklist (Step 2).")
        except Exception as e:
            print(f"[ERROR] Failed to click Proceed button: {str(e)}")
            raise

    def create_rfi(self):
        print("\n=== START RFI CREATION ===")
        self.open_form()
        self.fill_form()
        self.submit_form()
        print("=== END RFI CREATION ===")
