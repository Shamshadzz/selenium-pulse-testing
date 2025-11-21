from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class FinalApprovalPage(BasePage):
    """Quality Inspector - Final Approval Page
    
    Features:
    - Navigate to inspected RFIs
    - View inspection results
    - Provide final quality approval
    - Add final remarks
    """

    # Navigation
    INSPECTION_MENU = (By.XPATH, "//a[contains(text(), 'Inspection') or contains(text(), 'Quality')]")
    INSPECTED_TAB = (By.XPATH, "//button[contains(text(), 'Inspected') or contains(text(), 'Completed')]")
    
    # RFI List
    FIRST_RFI_ROW = (By.XPATH, "(//table//tr[@data-testid='rfi-row' or contains(@class, 'table-row')])[1]")
    FINAL_APPROVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Final Approve') or contains(text(), 'Close')]")
    
    # Final Approval Form
    FINAL_REMARKS_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Enter final remarks' or @name='remarks']")
    CONFIRM_FINAL_APPROVAL_BUTTON = (By.XPATH, "//button[@type='submit' or contains(text(), 'Confirm')]")
    
    # Success Messages
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(), 'successfully') or contains(text(), 'Success') or contains(text(), 'closed')]")

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

    def go_to_inspected_list(self):
        """Click on inspected RFIs tab."""
        print("[ACTION] Opening inspected RFIs...")
        try:
            inspected_tab = self.wait.until(EC.element_to_be_clickable(self.INSPECTED_TAB))
            inspected_tab.click()
            time.sleep(0.5)
            print("[SUCCESS] Opened inspected RFIs")
        except Exception as e:
            print(f"[WARNING] Inspected tab not found: {str(e)}")

    def open_first_rfi(self):
        """Open the first RFI for final approval."""
        print("[ACTION] Opening first RFI for final approval...")
        try:
            first_rfi = self.wait.until(EC.element_to_be_clickable(self.FIRST_RFI_ROW))
            first_rfi.click()
            time.sleep(0.5)
            print("[SUCCESS] Opened RFI")
        except Exception as e:
            print(f"[ERROR] Failed to open RFI: {str(e)}")
            raise

    def add_final_remarks(self, remarks):
        """Add final approval remarks.
        
        Args:
            remarks: Final remarks text
        """
        print(f"[ACTION] Adding final remarks: {remarks}")
        try:
            remarks_field = self.wait.until(EC.visibility_of_element_located(self.FINAL_REMARKS_TEXTAREA))
            remarks_field.clear()
            remarks_field.send_keys(remarks)
            print("[SUCCESS] Added final remarks")
        except Exception as e:
            print(f"[WARNING] Could not add final remarks: {str(e)}")

    def click_final_approve(self):
        """Click the final approve button."""
        print("[ACTION] Clicking Final Approve...")
        try:
            approve_btn = self.wait.until(EC.element_to_be_clickable(self.FINAL_APPROVE_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", approve_btn)
            time.sleep(0.2)
            approve_btn.click()
            print("[SUCCESS] Clicked Final Approve")
        except Exception as e:
            print(f"[ERROR] Failed to click final approve: {str(e)}")
            raise

    def confirm_final_approval(self):
        """Confirm the final approval."""
        print("[ACTION] Confirming final approval...")
        try:
            confirm_btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_FINAL_APPROVAL_BUTTON))
            confirm_btn.click()
            time.sleep(0.5)
            print("[SUCCESS] Final approval confirmed")
        except Exception as e:
            print(f"[ERROR] Failed to confirm final approval: {str(e)}")
            raise

    def is_success_displayed(self):
        """Check if success message is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except:
            return False

    def give_final_approval(self, remarks="Quality inspection passed. RFI closed."):
        """Complete final approval workflow.
        
        Args:
            remarks: Final remarks (default: "Quality inspection passed. RFI closed.")
        """
        print("\n=== STARTING FINAL APPROVAL WORKFLOW ===")
        
        self.go_to_inspected_list()
        self.open_first_rfi()
        self.add_final_remarks(remarks)
        self.click_final_approve()
        self.confirm_final_approval()
        
        print("=== FINAL APPROVAL COMPLETED ===\n")
