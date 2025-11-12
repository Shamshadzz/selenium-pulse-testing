from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from pages.base_page import BasePage
from config.config import Config
import time


class CreateRfiPage(BasePage):
    """
    Page Object for Create RFI form with hierarchical dependency handling.
    
    COMPLETE DEPENDENCY HIERARCHY (Cascading):
    ┌─────────────────────────────────────────────────────────────┐
    │ Plot No.                                                     │
    │   └─> Block No.                                             │
    │         └─> Package                                         │
    │               └─> Sub-Package                               │
    │                     └─> Activity                            │
    │                           └─> Sub-Activity                  │
    │                                 └─> Location                │
    │                                 └─> Inspection Checkpoint   │
    │                                       └─> Inspection Checklist│
    └─────────────────────────────────────────────────────────────┘
    
    Each field depends on ALL fields above it in the hierarchy.
    Selecting any parent field will reset/reload all child fields below.
    """

    # --- LOCATORS ---
    CREATE_RFI_BUTTON = (By.XPATH, "//button[normalize-space()='Create RFI']")
    FORM_CONTAINER = (By.CSS_SELECTOR, ".steps__content.h_full.ov_auto")

    # Dropdown triggers - Using multiple strategies for reliability
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

    # Success toast
    SUCCESS_TOAST = (By.XPATH, "//*[contains(text(),'successfully') or contains(text(),'Success')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 30)
        self.short_wait = WebDriverWait(driver, 5)

    # --- UTILITY METHODS ---

    def scroll_into_view(self, element):
        """Scroll element into view within its container."""
        try:
            self.driver.execute_script("""
                const elem = arguments[0];
                const container = elem.closest('.steps__content, .ov_auto, [data-part="content"]');
                if (container) {
                    container.scrollTo({
                        top: elem.offsetTop - container.clientHeight / 2,
                        behavior: 'auto'
                    });
                } else {
                    elem.scrollIntoView({behavior: 'auto', block: 'center'});
                }
            """, element)
            time.sleep(0.3)
        except Exception as e:
            print(f"[WARN] Scroll failed: {e}")

    def wait_for_dependent_field_ready(self, trigger_locator, field_name, timeout=30):
        """
        Wait for a dependent dropdown field to be ready after parent selection.
        This checks:
        1. Field is not disabled
        2. Field has loaded options (checks hidden select)
        3. Field is stable (no re-renders)
        
        Args:
            trigger_locator: Tuple of (By, locator) for the field's trigger button
            field_name: Human-readable name for logging
            timeout: Maximum seconds to wait
        """
        print(f"[DEBUG] Waiting for dependent field '{field_name}' to be ready...")
        end_time = time.time() + timeout
        last_status = ""
        options_count = 0
        
        while time.time() < end_time:
            try:
                # Find the trigger button
                trigger = self.driver.find_element(*trigger_locator)
                
                # Check 1: Not disabled (multiple attributes to check)
                disabled = trigger.get_attribute('disabled')
                data_disabled = trigger.get_attribute('data-disabled')
                aria_disabled = trigger.get_attribute('aria-disabled')
                
                if disabled or data_disabled == 'true' or aria_disabled == 'true':
                    status = "disabled"
                    if status != last_status:
                        print(f"[WAIT] Field '{field_name}' is currently {status}")
                        last_status = status
                    time.sleep(1)
                    continue
                
                # Check 2: Has loaded options (check hidden select element)
                try:
                    # Find the parent select component
                    field_root = trigger.find_element(By.XPATH, "./ancestor::div[@data-scope='select' or @data-scope='combobox']")
                    select_element = field_root.find_element(By.TAG_NAME, 'select')
                    options = select_element.find_elements(By.TAG_NAME, 'option')
                    
                    # Filter out empty placeholder options
                    real_options = [opt for opt in options if opt.get_attribute('value') and opt.get_attribute('value').strip()]
                    current_options_count = len(real_options)
                    
                    if current_options_count == 0:
                        status = "enabled but no options loaded"
                        if status != last_status:
                            print(f"[WAIT] Field '{field_name}': {status} (waiting for API response...)")
                            last_status = status
                        time.sleep(1)
                        continue
                    
                    # Log when options change (indicates backend loaded new data)
                    if current_options_count != options_count:
                        print(f"[PROGRESS] Field '{field_name}' now has {current_options_count} option(s)")
                        options_count = current_options_count
                    
                except Exception as e:
                    print(f"[WARN] Could not check options for '{field_name}': {e}")
                    # If we can't check options but field is enabled, we'll proceed after stability check
                    pass
                
                # Check 3: Element is stable (access twice to detect re-renders)
                trigger.is_displayed()
                time.sleep(0.5)
                trigger = self.driver.find_element(*trigger_locator)
                trigger.is_displayed()
                
                print(f"[READY] ✓ Field '{field_name}' is ready with {options_count} option(s)!")
                return trigger
                
            except StaleElementReferenceException:
                print(f"[WAIT] Field '{field_name}' - re-rendering, retrying...")
                time.sleep(1)
                continue
            except Exception as e:
                if "no such element" not in str(e).lower():
                    print(f"[DEBUG] Field '{field_name}' - {str(e)[:100]}")
                time.sleep(1)
                continue
        
        # Timeout - take screenshot and provide detailed error
        screenshot_path = f"field_not_ready_{field_name.replace(' ', '_')}_{int(time.time())}.png"
        self.driver.save_screenshot(screenshot_path)
        
        # Try to get current state for debugging
        try:
            trigger = self.driver.find_element(*trigger_locator)
            disabled_state = trigger.get_attribute('disabled')
            print(f"[ERROR] Field '{field_name}' final state - disabled: {disabled_state}")
        except:
            pass
        
        raise TimeoutException(
            f"Dependent field '{field_name}' did not become ready within {timeout}s. "
            f"Screenshot saved: {screenshot_path}"
        )

    def safe_click(self, locator, retry=3):
        """Click element with retry logic and JS fallback."""
        print(f"[DEBUG] Clicking: {locator}")
        
        for attempt in range(retry):
            try:
                element = self.wait.until(EC.presence_of_element_located(locator))
                self.wait.until(EC.visibility_of_element_located(locator))
                self.scroll_into_view(element)
                
                # Wait for clickability
                clickable = self.wait.until(EC.element_to_be_clickable(locator))
                
                # Try JavaScript click first (more reliable for React)
                try:
                    self.driver.execute_script("arguments[0].click();", clickable)
                    print(f"[DEBUG] JS clicked successfully")
                    return clickable
                except Exception:
                    # Fallback to regular click
                    clickable.click()
                    print(f"[DEBUG] Regular clicked successfully")
                    return clickable
                    
            except StaleElementReferenceException:
                print(f"[WARN] Stale element on attempt {attempt + 1}, retrying...")
                time.sleep(1)
            except Exception as e:
                print(f"[WARN] Click failed on attempt {attempt + 1}: {e}")
                if attempt == retry - 1:
                    self.driver.save_screenshot(f"click_error_{int(time.time())}.png")
                    raise
                time.sleep(1)

    def safe_input(self, locator, text):
        """Input text and blur."""
        print(f"[DEBUG] Typing '{text}' into {locator}")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.scroll_into_view(element)
        element.clear()
        element.send_keys(text)
        element.send_keys(Keys.TAB)
        print(f"[DEBUG] Input completed")
        time.sleep(0.5)
        return element

    def select_dropdown_with_dependency_wait(self, trigger_locator, option_text, 
                                            dependent_field_locator=None, 
                                            dependent_field_name=None):
        """
        Select a dropdown option and optionally wait for dependent field to load.
        This is the key method for handling hierarchical dependencies.
        """
        print(f"\n{'='*70}")
        print(f"[DROPDOWN] Selecting '{option_text}'")
        print(f"{'='*70}")
        
        # Step 1: Open dropdown
        print(f"[STEP 1] Opening dropdown...")
        trigger = self.safe_click(trigger_locator)
        
        # Step 2: Wait for dropdown panel
        print(f"[STEP 2] Waiting for dropdown panel to open...")
        dropdown_opened = False
        for attempt in range(3):
            try:
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-part='content' and @data-state='open']")
                ))
                time.sleep(0.5)
                dropdown_opened = True
                print(f"[STEP 2] Dropdown panel opened")
                break
            except TimeoutException:
                print(f"[WARN] Dropdown not open (attempt {attempt + 1}), retrying click...")
                trigger = self.safe_click(trigger_locator, retry=1)
                time.sleep(0.5)
        
        if not dropdown_opened:
            self.driver.save_screenshot(f"dropdown_not_open_{option_text}.png")
            raise Exception(f"Dropdown did not open after 3 attempts")

        # Step 3: Click the option
        print(f"[STEP 3] Clicking option '{option_text}'...")
        option_xpath = f"//div[@data-part='content' and @data-state='open']//span[@data-part='item-text' and normalize-space()='{option_text}']"
        
        try:
            option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            self.scroll_into_view(option)
            self.driver.execute_script("arguments[0].click();", option)
            print(f"[STEP 3] Option '{option_text}' clicked")
        except TimeoutException:
            # List available options
            try:
                available = self.driver.find_elements(
                    By.XPATH, 
                    "//div[@data-part='content' and @data-state='open']//span[@data-part='item-text']"
                )
                print(f"[ERROR] Available options: {[opt.text for opt in available]}")
            except:
                pass
            self.driver.save_screenshot(f"option_not_found_{option_text}.png")
            raise Exception(f"Option '{option_text}' not found")

        # Step 4: Wait for dropdown to close
        print(f"[STEP 4] Waiting for dropdown to close...")
        try:
            self.wait.until(EC.invisibility_of_element_located(
                (By.XPATH, "//div[@data-part='content' and @data-state='open']")
            ))
            print(f"[STEP 4] Dropdown closed")
        except TimeoutException:
            print(f"[WARN] Dropdown did not close cleanly")

        # Step 5: Wait for dependent field if specified
        if dependent_field_locator and dependent_field_name:
            print(f"\n[STEP 5] Waiting for dependent field '{dependent_field_name}' to load...")
            self.wait_for_dependent_field_ready(
                dependent_field_locator, 
                dependent_field_name, 
                timeout=30
            )
            print(f"[STEP 5] Dependent field '{dependent_field_name}' is ready")
        else:
            # Just wait a bit for React state to settle
            print(f"[STEP 5] Waiting for React state to settle (2 seconds)...")
            time.sleep(2)
        
        print(f"[SUCCESS] Completed selection of '{option_text}'")
        print(f"{'='*70}\n")

    # --- MAIN ACTIONS ---

    def navigate(self):
        print(f"[DEBUG] Navigating to {Config.BASE_URL}/welcome")
        self.driver.get(f"{Config.BASE_URL}/welcome")
        self.wait_for_page_load()
        print("[DEBUG] Page loaded successfully.")

    def open_form(self):
        print("\n[ACTION] Opening Create RFI form...")
        self.safe_click(self.CREATE_RFI_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.FORM_CONTAINER))
        time.sleep(1)
        print("[SUCCESS] Create RFI form opened\n")

    def fill_form(self):
        print("\n" + "="*70)
        print("STARTING RFI FORM FILL PROCESS")
        print("="*70)
        print("\nDEPENDENCY HIERARCHY:")
        print("Plot → Block → Package → Sub-Package → Activity → Sub-Activity")
        print("                                         ↓")
        print("                        Location + Inspection Fields")
        print("="*70 + "\n")

        # LEVEL 1: Plot No. (Root - no dependencies)
        # Selecting Plot will trigger Block options to load
        self.select_dropdown_with_dependency_wait(
            trigger_locator=self.PLOT_TRIGGER,
            option_text="S05b",
            dependent_field_locator=self.BLOCK_TRIGGER,
            dependent_field_name="Block No."
        )
        
        # LEVEL 2: Block No. (depends on: Plot)
        # Selecting Block will trigger Package options to load
        self.select_dropdown_with_dependency_wait(
            trigger_locator=self.BLOCK_TRIGGER,
            option_text="BL05",
            dependent_field_locator=self.PACKAGE_TRIGGER,
            dependent_field_name="Package"
        )
        
        # LEVEL 3: Package (depends on: Plot, Block)
        # Selecting Package will trigger Sub-Package options to load
        # This is often the most critical dependency as it's a backend API call
        self.select_dropdown_with_dependency_wait(
            trigger_locator=self.PACKAGE_TRIGGER,
            option_text="Civil",
            dependent_field_locator=self.SUBPACKAGE_TRIGGER,
            dependent_field_name="Sub-Package"
        )
        
        # LEVEL 4: Sub-Package (depends on: Plot, Block, Package)
        # Selecting Sub-Package will trigger Activity options to load
        self.select_dropdown_with_dependency_wait(
            trigger_locator=self.SUBPACKAGE_TRIGGER,
            option_text="MMS Installation",
            dependent_field_locator=self.ACTIVITY_TRIGGER,
            dependent_field_name="Activity"
        )
        
        # LEVEL 5: Activity (depends on: Plot, Block, Package, Sub-Package)
        # Selecting Activity will trigger Sub-Activity options to load
        self.select_dropdown_with_dependency_wait(
            trigger_locator=self.ACTIVITY_TRIGGER,
            option_text="MMS Installation",
            dependent_field_locator=self.SUBACTIVITY_TRIGGER,
            dependent_field_name="Sub-Activity"
        )
        
        # LEVEL 6: Sub-Activity (depends on: Plot, Block, Package, Sub-Package, Activity)
        # Selecting Sub-Activity will trigger:
        #   - Location field to become available
        #   - Inspection Checkpoint options to load (based on Activity/Sub-Activity)
        print("\n[INFO] Sub-Activity selection will trigger multiple dependent fields:")
        print("       - Location field")
        print("       - Inspection Checkpoint options")
        print("       - Inspection Checklist options (dependent on Checkpoint)")
        
        self.select_dropdown_with_dependency_wait(
            trigger_locator=self.SUBACTIVITY_TRIGGER,
            option_text="MMS Installation",
            dependent_field_locator=self.LOCATION_INPUT,
            dependent_field_name="Location"
        )
        
        # Additional wait for inspection fields to load
        # These depend on the Activity/Sub-Activity combination
        print("\n[INFO] Waiting for Inspection Checkpoint field to load options...")
        time.sleep(2)  # Extra buffer for inspection fields
        
        # LEVEL 7: Text Input Fields (depend on full hierarchy above)
        print("\n" + "="*70)
        print("[SECTION] FILLING TEXT INPUT FIELDS")
        print("="*70)
        
        # Location - depends on entire hierarchy
        print("\n[FIELD] Location (depends on: all above selections)")
        self.safe_input(self.LOCATION_INPUT, "R01-T01")
        
        # Quantity - independent field
        print("\n[FIELD] Quantity (independent)")
        self.safe_input(self.QUANTITY_INPUT, "25")
        
        # LEVEL 8: Unit of Measurement (independent)
        print("\n" + "="*70)
        print("[SECTION] UNIT OF MEASUREMENT (Independent)")
        print("="*70)
        self.select_dropdown_with_dependency_wait(
            trigger_locator=self.UNIT_TRIGGER,
            option_text="MTR"
        )
        
        # Subcontractor - independent field
        print("\n[FIELD] Subcontractor Name (independent)")
        self.safe_input(self.SUBCONTRACTOR_INPUT, "TechBuild Contractors Pvt Ltd")
        
        # LEVEL 9: Inspection Fields (depend on Activity/Sub-Activity)
        print("\n" + "="*70)
        print("[SECTION] INSPECTION FIELDS")
        print("These depend on: Activity + Sub-Activity selections")
        print("="*70)
        
        # Inspection Checkpoint - depends on Activity/Sub-Activity
        # Selecting Checkpoint will trigger Checklist options to load
        self.select_dropdown_with_dependency_wait(
            trigger_locator=self.INSPECTION_CHECKPOINT_TRIGGER,
            option_text="If Tracker: Tracker Alignment, Tightening & Torquing up to Torque Tube incl. Transmission Shaft If Fixed Tilt: Fixed Tilt Alignment, Tightening & Torquing up to bracing, perlin and all asembly parts",
            dependent_field_locator=self.INSPECTION_CHECKLIST_TRIGGER,
            dependent_field_name="Inspection Checklist"
        )
        
        # LEVEL 10: Inspection Checklist (depends on: Checkpoint selection)
        self.select_dropdown_with_dependency_wait(
            trigger_locator=self.INSPECTION_CHECKLIST_TRIGGER,
            option_text="PV Module Mounting Structure Installation Protocol - Tracker"
        )

        print("\n" + "="*70)
        print("✓ RFI FORM FILL COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nSUMMARY:")
        print("  - Hierarchical fields: 10 levels deep")
        print("  - All dependencies resolved successfully")
        print("  - Form ready for submission")
        print("="*70 + "\n")

    def submit_form(self):
        print("\n[ACTION] Submitting RFI form...")
        try:
            self.safe_click(self.PROCEED_BUTTON)
            print("[DEBUG] Proceed button clicked")
            time.sleep(1)
        except Exception as e:
            print(f"[INFO] Proceed button not found/needed: {e}")
        
        self.safe_click(self.SUBMIT_BUTTON)
        print("[DEBUG] Submit button clicked")
        
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_TOAST))
        print("\n[SUCCESS] ✓ RFI SUBMITTED SUCCESSFULLY!\n")

    def create_rfi(self):
        """End-to-end Create RFI flow with full dependency chain handling."""
        print("\n" + "="*70)
        print("START: CREATE RFI PROCESS")
        print("="*70)
        
        self.open_form()
        self.fill_form()
        self.submit_form()
        
        print("="*70)
        print("END: CREATE RFI PROCESS - SUCCESS ✓")
        print("="*70 + "\n")