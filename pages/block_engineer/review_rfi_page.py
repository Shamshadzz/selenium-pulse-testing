from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class ReviewRfiPage(BasePage):
    """Block Engineer - Review RFI Page
    
    Features:
    - Navigate to RFI list/pending reviews
    - View RFI details
    - Add review comments
    - Approve or request changes
    """

    # Navigation
    RFI_LIST_MENU = (By.XPATH, "//a[contains(text(), 'RFI') or contains(text(), 'Requests')]")
    PENDING_TAB = (By.XPATH, "//button[contains(text(), 'Pending') or contains(text(), 'Review')]")
    
    # RFI List
    FIRST_RFI_ROW = (By.XPATH, "(//table//tr[@data-testid='rfi-row' or contains(@class, 'table-row')])[1]")
    VIEW_BUTTON = (By.XPATH, "//button[contains(text(), 'View') or contains(text(), 'Details')]")
    
    # Review Section
    REVIEW_COMMENTS_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Enter review comments' or @name='comments']")
    APPROVE_BUTTON = (By.XPATH, "//button[normalize-space()='Approve' or contains(text(), 'Approve')]")
    REQUEST_CHANGES_BUTTON = (By.XPATH, "//button[contains(text(), 'Request Changes') or contains(text(), 'Reject')]")
    SUBMIT_REVIEW_BUTTON = (By.XPATH, "//button[@type='submit' or contains(text(), 'Submit Review')]")
    
    # Success/Error Messages
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(), 'successfully') or contains(text(), 'Success')]")
    ERROR_MESSAGE = (By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        """Navigate to RFI review page."""
        print("[INFO] Navigating to RFI review page...")
        try:
            rfi_menu = self.wait.until(EC.element_to_be_clickable(self.RFI_LIST_MENU))
            rfi_menu.click()
            time.sleep(0.5)
            print("[SUCCESS] Navigated to RFI list")
        except Exception as e:
            print(f"[ERROR] Failed to navigate: {str(e)}")
            raise

    def go_to_pending_reviews(self):
        """Click on pending reviews tab."""
        print("[ACTION] Opening pending reviews...")
        try:
            pending_tab = self.wait.until(EC.element_to_be_clickable(self.PENDING_TAB))
            pending_tab.click()
            time.sleep(0.5)
            print("[SUCCESS] Opened pending reviews")
        except Exception as e:
            print(f"[WARNING] Pending tab not found or already on pending view: {str(e)}")

    def open_first_rfi(self):
        """Open the first RFI in the list."""
        print("[ACTION] Opening first RFI for review...")
        try:
            first_rfi = self.wait.until(EC.element_to_be_clickable(self.FIRST_RFI_ROW))
            first_rfi.click()
            time.sleep(0.5)
            
            # Try to click View button if exists
            try:
                view_btn = self.wait.until(EC.element_to_be_clickable(self.VIEW_BUTTON))
                view_btn.click()
                time.sleep(0.5)
            except:
                pass  # View button may not exist if RFI opens directly
            
            print("[SUCCESS] Opened RFI for review")
        except Exception as e:
            print(f"[ERROR] Failed to open RFI: {str(e)}")
            raise

    def add_review_comments(self, comments):
        """Add review comments to the RFI.
        
        Args:
            comments: Review comments text
        """
        print(f"[ACTION] Adding review comments: {comments}")
        try:
            comments_field = self.wait.until(EC.visibility_of_element_located(self.REVIEW_COMMENTS_TEXTAREA))
            comments_field.clear()
            comments_field.send_keys(comments)
            print("[SUCCESS] Added review comments")
        except Exception as e:
            print(f"[ERROR] Failed to add comments: {str(e)}")
            raise

    def approve_rfi(self):
        """Approve the RFI."""
        print("[ACTION] Approving RFI...")
        try:
            approve_btn = self.wait.until(EC.element_to_be_clickable(self.APPROVE_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", approve_btn)
            time.sleep(0.2)
            approve_btn.click()
            print("[SUCCESS] Clicked Approve button")
        except Exception as e:
            print(f"[ERROR] Failed to approve: {str(e)}")
            raise

    def request_changes(self):
        """Request changes to the RFI."""
        print("[ACTION] Requesting changes...")
        try:
            request_btn = self.wait.until(EC.element_to_be_clickable(self.REQUEST_CHANGES_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", request_btn)
            time.sleep(0.2)
            request_btn.click()
            print("[SUCCESS] Clicked Request Changes button")
        except Exception as e:
            print(f"[ERROR] Failed to request changes: {str(e)}")
            raise

    def submit_review(self):
        """Submit the review."""
        print("[ACTION] Submitting review...")
        try:
            submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_REVIEW_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", submit_btn)
            time.sleep(0.2)
            submit_btn.click()
            time.sleep(0.5)
            print("[SUCCESS] Review submitted")
        except Exception as e:
            print(f"[ERROR] Failed to submit review: {str(e)}")
            raise

    def is_success_displayed(self):
        """Check if success message is displayed."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except:
            return False

    def review_rfi(self, comments="Reviewed and approved", approve=True):
        """Complete RFI review workflow.
        
        Args:
            comments: Review comments (default: "Reviewed and approved")
            approve: True to approve, False to request changes
        """
        print("\n=== STARTING RFI REVIEW WORKFLOW ===")
        
        self.go_to_pending_reviews()
        self.open_first_rfi()
        self.add_review_comments(comments)
        
        if approve:
            self.approve_rfi()
        else:
            self.request_changes()
        
        self.submit_review()
        
        print("=== RFI REVIEW COMPLETED ===\n")
