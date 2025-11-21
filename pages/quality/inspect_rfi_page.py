from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class InspectRfiPage(BasePage):
    """Quality Inspector - Inspect RFI Page
    
    Features:
    - Navigate to RFI inspection queue
    - View RFI details and inspection checklist
    - Perform quality inspection
    - Add inspection findings
    - Mark as pass/fail
    """

    # Navigation
    INSPECTION_MENU = (By.XPATH, "//a[contains(text(), 'Inspection') or contains(text(), 'Quality')]")
    PENDING_INSPECTIONS_TAB = (By.XPATH, "//button[contains(text(), 'Pending') or contains(text(), 'Queue')]")
    
    # RFI List
    FIRST_RFI_ROW = (By.XPATH, "(//table//tr[@data-testid='rfi-row' or contains(@class, 'table-row')])[1]")
    INSPECT_BUTTON = (By.XPATH, "//button[contains(text(), 'Inspect') or contains(text(), 'Start Inspection')]")
    
    # Inspection Form
    INSPECTION_FINDINGS_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Enter inspection findings' or @name='findings']")
    PASS_CHECKBOX = (By.XPATH, "//input[@type='checkbox' and (@name='pass' or @value='pass')]")
    FAIL_CHECKBOX = (By.XPATH, "//input[@type='checkbox' and (@name='fail' or @value='fail')]")
    PASS_RADIO = (By.XPATH, "//input[@type='radio' and @value='pass']")
    FAIL_RADIO = (By.XPATH, "//input[@type='radio' and @value='fail']")
    
    # Quality Checks
    QUALITY_CHECKLIST_ITEMS = (By.XPATH, "//input[@type='checkbox' and contains(@name, 'quality')]")
    
    # Submit
    SUBMIT_INSPECTION_BUTTON = (By.XPATH, "//button[@type='submit' or contains(text(), 'Submit Inspection')]")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirm')]")
    
    # Success Messages
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(), 'successfully') or contains(text(), 'Success') or contains(text(), 'completed')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        """Navigate to inspection page."""
        print("[INFO] Navigating to inspection page...")
        try:
            inspection_menu = self.wait.until(EC.element_to_be_clickable(self.INSPECTION_MENU))
            inspection_menu.click()
            time.sleep(0.5)
            print("[SUCCESS] Navigated to inspection page")
        except Exception as e:
            print(f"[ERROR] Failed to navigate: {str(e)}")
            raise

    def go_to_pending_inspections(self):
        """Click on pending inspections tab."""
        print("[ACTION] Opening pending inspections...")
        try:
            pending_tab = self.wait.until(EC.element_to_be_clickable(self.PENDING_INSPECTIONS_TAB))
            pending_tab.click()
            time.sleep(0.5)
            print("[SUCCESS] Opened pending inspections")
        except Exception as e:
            print(f"[WARNING] Pending tab not found: {str(e)}")

    def open_first_rfi(self):
        """Open the first RFI for inspection."""
        print("[ACTION] Opening first RFI for inspection...")
        try:
            first_rfi = self.wait.until(EC.element_to_be_clickable(self.FIRST_RFI_ROW))
            first_rfi.click()
            time.sleep(0.5)
            
            # Try to click Inspect button if exists
            try:
                inspect_btn = self.wait.until(EC.element_to_be_clickable(self.INSPECT_BUTTON))
                inspect_btn.click()
                time.sleep(0.5)
            except:
                pass  # Inspect button may not exist
            
            print("[SUCCESS] Opened RFI for inspection")
        except Exception as e:
            print(f"[ERROR] Failed to open RFI: {str(e)}")
            raise

    def add_inspection_findings(self, findings):
        """Add inspection findings.
        
        Args:
            findings: Inspection findings text
        """
        print(f"[ACTION] Adding inspection findings: {findings}")
        try:
            findings_field = self.wait.until(EC.visibility_of_element_located(self.INSPECTION_FINDINGS_TEXTAREA))
            findings_field.clear()
            findings_field.send_keys(findings)
            print("[SUCCESS] Added inspection findings")
        except Exception as e:
            print(f"[WARNING] Could not add findings: {str(e)}")

    def complete_quality_checklist(self):
        """Check all quality checklist items."""
        print("[ACTION] Completing quality checklist...")
        try:
            checklist_items = self.driver.find_elements(*self.QUALITY_CHECKLIST_ITEMS)
            if checklist_items:
                for idx, item in enumerate(checklist_items):
                    if not item.is_selected():
                        self.driver.execute_script("arguments[0].click();", item)
                        time.sleep(0.1)
                print(f"[SUCCESS] Checked {len(checklist_items)} quality items")
            else:
                print("[INFO] No quality checklist items found")
        except Exception as e:
            print(f"[WARNING] Could not complete checklist: {str(e)}")

    def mark_as_pass(self):
        """Mark inspection as passed."""
        print("[ACTION] Marking as PASS...")
        try:
            # Try radio button first
            try:
                pass_radio = self.wait.until(EC.element_to_be_clickable(self.PASS_RADIO))
                self.driver.execute_script("arguments[0].click();", pass_radio)
                print("[SUCCESS] Marked as PASS (radio)")
                return
            except:
                pass
            
            # Try checkbox
            try:
                pass_checkbox = self.wait.until(EC.element_to_be_clickable(self.PASS_CHECKBOX))
                if not pass_checkbox.is_selected():
                    self.driver.execute_script("arguments[0].click();", pass_checkbox)
                print("[SUCCESS] Marked as PASS (checkbox)")
                return
            except:
                pass
            
            print("[WARNING] Could not find pass option")
        except Exception as e:
            print(f"[ERROR] Failed to mark as pass: {str(e)}")

    def mark_as_fail(self):
        """Mark inspection as failed."""
        print("[ACTION] Marking as FAIL...")
        try:
            # Try radio button first
            try:
                fail_radio = self.wait.until(EC.element_to_be_clickable(self.FAIL_RADIO))
                self.driver.execute_script("arguments[0].click();", fail_radio)
                print("[SUCCESS] Marked as FAIL (radio)")
                return
            except:
                pass
            
            # Try checkbox
            try:
                fail_checkbox = self.wait.until(EC.element_to_be_clickable(self.FAIL_CHECKBOX))
                if not fail_checkbox.is_selected():
                    self.driver.execute_script("arguments[0].click();", fail_checkbox)
                print("[SUCCESS] Marked as FAIL (checkbox)")
                return
            except:
                pass
            
            print("[WARNING] Could not find fail option")
        except Exception as e:
            print(f"[ERROR] Failed to mark as fail: {str(e)}")

    def submit_inspection(self):
        """Submit the inspection."""
        print("[ACTION] Submitting inspection...")
        try:
            submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_INSPECTION_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", submit_btn)
            time.sleep(0.2)
            submit_btn.click()
            time.sleep(0.5)
            
            # Handle confirmation dialog if exists
            try:
                confirm_btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON))
                confirm_btn.click()
                time.sleep(0.3)
            except:
                pass  # No confirmation needed
            
            print("[SUCCESS] Inspection submitted")
        except Exception as e:
            print(f"[ERROR] Failed to submit inspection: {str(e)}")
            raise

    def is_inspection_complete(self):
        """Check if inspection completion message is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except:
            return False

    def perform_inspection(self, findings="All quality standards met", passed=True):
        """Complete RFI inspection workflow.
        
        Args:
            findings: Inspection findings (default: "All quality standards met")
            passed: True to mark as pass, False to mark as fail
        """
        print("\n=== STARTING RFI INSPECTION WORKFLOW ===")
        
        self.go_to_pending_inspections()
        self.open_first_rfi()
        self.complete_quality_checklist()
        self.add_inspection_findings(findings)
        
        if passed:
            self.mark_as_pass()
        else:
            self.mark_as_fail()
        
        self.submit_inspection()
        
        print("=== RFI INSPECTION COMPLETED ===\n")
