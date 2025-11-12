from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from pages.base_page import BasePage
from config.config import Config


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
        self.wait = WebDriverWait(driver, 5)

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

        # Open dropdown
        trigger = self.safe_click(trigger_locator)
        dropdown_open = (By.XPATH, "//div[@data-part='content' and @data-state='open']")
        self.wait.until(EC.presence_of_element_located(dropdown_open))

        # Select each option
        for opt_text in options:
            opt_xpath = f"//div[@data-part='content']//span[normalize-space()='{opt_text}']"
            option = self.wait.until(EC.element_to_be_clickable((By.XPATH, opt_xpath)))
            self.scroll_into_view(option)
            self.driver.execute_script("arguments[0].click();", option)
            print(f"[SUCCESS] Selected '{opt_text}'")

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

    def open_form(self):
        print("[INFO] Opening Create RFI form...")
        self.safe_click(self.CREATE_RFI_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.FORM_CONTAINER))
        print("[SUCCESS] Form opened.")

    def fill_form(self):
        print("=== START FORM FILL ===")
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
        print("[ACTION] Submitting form...")
        try:
            self.safe_click(self.PROCEED_BUTTON)
        except Exception:
            pass
        self.safe_click(self.SUBMIT_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_TOAST))
        print("[SUCCESS] RFI submitted successfully.")

    def create_rfi(self):
        print("\n=== START RFI CREATION ===")
        self.open_form()
        self.fill_form()
        self.submit_form()
        print("=== END RFI CREATION ===")
