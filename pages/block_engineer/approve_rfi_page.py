from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class ApproveRfiPage(BasePage):
    """Block Engineer - Approve RFI Page (Final Approval)
    
    Features:
    - Navigate to approved RFI list
    - View RFI details
    - Provide final approval
    - Add approval notes
    """

    # Navigation
    RFI_LIST_MENU = (By.XPATH, "//a[contains(text(), 'RFI') or contains(text(), 'Requests')]")
    APPROVED_TAB = (By.XPATH, "//button[contains(text(), 'Approved') or contains(text(), 'Final')]")
    
    # RFI List
    FIRST_RFI_ROW = (By.XPATH, "(//table//tr[@data-testid='rfi-row' or contains(@class, 'table-row')])[1]")
    APPROVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Final Approve') or contains(text(), 'Approve')]")
    
    # Approval Section
    APPROVAL_NOTES_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Enter approval notes' or @name='notes']")
    CONFIRM_APPROVE_BUTTON = (By.XPATH, "//button[@type='submit' or contains(text(), 'Confirm')]")
    
    # Success Messages
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(), 'successfully') or contains(text(), 'Success')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        """Navigate to RFI approval page."""
        print("[INFO] Navigating to RFI approval page...")
        try:
            rfi_menu = self.wait.until(EC.element_to_be_clickable(self.RFI_LIST_MENU))
            rfi_menu.click()
            time.sleep(0.5)
            print("[SUCCESS] Navigated to RFI list")
        except Exception as e:
            print(f"[ERROR] Failed to navigate: {str(e)}")
            raise

    def go_to_approved_list(self):
        """Click on approved RFIs tab."""
        print("[ACTION] Opening approved RFIs...")
        try:
            approved_tab = self.wait.until(EC.element_to_be_clickable(self.APPROVED_TAB))
            approved_tab.click()
            time.sleep(0.5)
            print("[SUCCESS] Opened approved RFIs")
        except Exception as e:
            print(f"[WARNING] Approved tab not found: {str(e)}")

    def open_first_rfi(self):
        """Open the first RFI in the list."""
        print("[ACTION] Opening first RFI for final approval...")
        try:
            first_rfi = self.wait.until(EC.element_to_be_clickable(self.FIRST_RFI_ROW))
            first_rfi.click()
            time.sleep(0.5)
            print("[SUCCESS] Opened RFI")
        except Exception as e:
            print(f"[ERROR] Failed to open RFI: {str(e)}")
            raise

    def add_approval_notes(self, notes):
        """Add approval notes.
        
        Args:
            notes: Approval notes text
        """
        print(f"[ACTION] Adding approval notes: {notes}")
        try:
            notes_field = self.wait.until(EC.visibility_of_element_located(self.APPROVAL_NOTES_TEXTAREA))
            notes_field.clear()
            notes_field.send_keys(notes)
            print("[SUCCESS] Added approval notes")
        except Exception as e:
            print(f"[WARNING] Could not add approval notes: {str(e)}")

    def click_approve(self):
        """Click the approve button."""
        print("[ACTION] Clicking Approve...")
        try:
            approve_btn = self.wait.until(EC.element_to_be_clickable(self.APPROVE_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", approve_btn)
            time.sleep(0.2)
            approve_btn.click()
            print("[SUCCESS] Clicked Approve")
        except Exception as e:
            print(f"[ERROR] Failed to click approve: {str(e)}")
            raise

    def confirm_approval(self):
        """Confirm the final approval."""
        print("[ACTION] Confirming approval...")
        try:
            confirm_btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_APPROVE_BUTTON))
            confirm_btn.click()
            time.sleep(0.5)
            print("[SUCCESS] Approval confirmed")
        except Exception as e:
            print(f"[ERROR] Failed to confirm approval: {str(e)}")
            raise

    def is_success_displayed(self):
        """Check if success message is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except:
            return False

    def approve_rfi(self, notes="Final approval granted"):
        """Complete RFI approval workflow.
        
        Args:
            notes: Approval notes (default: "Final approval granted")
        """
        print("\n=== STARTING RFI APPROVAL WORKFLOW ===")
        
        self.go_to_approved_list()
        self.open_first_rfi()
        self.add_approval_notes(notes)
        self.click_approve()
        self.confirm_approval()
        
        print("=== RFI APPROVAL COMPLETED ===\n")
