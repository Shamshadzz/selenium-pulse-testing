from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time


class InspectionChecklistPage(BasePage):
    """Inspection Checklist Page - Fills form after RFI submission."""

    # Form header
    FORM_TITLE = (By.XPATH, "//p[contains(text(), 'Inspection Checklist')]")
    
    # Page indicators
    PAGE_1_INDICATOR = (By.XPATH, "//p[contains(text(), 'Page 1/2')]")
    PAGE_2_INDICATOR = (By.XPATH, "//p[contains(text(), 'Page 2/2')]")
    
    # Navigation buttons
    PROCEED_BUTTON = (By.XPATH, "//button[normalize-space()='Proceed']")
    PREV_BUTTON = (By.CSS_SELECTOR, "button.steps__prev-trigger")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")
    
    # Page 1 Fields (not visible, but keeping for reference)
    PLOT_DROPDOWN = (By.XPATH, "//label[.//span[contains(text(), 'Plot No.')]]//following-sibling::div//button")
    BLOCK_DROPDOWN = (By.XPATH, "//label[.//span[contains(text(), 'Block No.')]]//following-sibling::div//button")
    PACKAGE_DROPDOWN = (By.XPATH, "//label[.//span[contains(text(), 'Package')]]//following-sibling::div//button")
    SUBPACKAGE_DROPDOWN = (By.XPATH, "//label[.//span[contains(text(), 'Sub-Package')]]//following-sibling::div//button")
    ACTIVITY_DROPDOWN = (By.XPATH, "//label[.//span[contains(text(), 'Activity')]]//following-sibling::div//button")
    SUBACTIVITY_DROPDOWN = (By.XPATH, "//label[.//span[contains(text(), 'Sub-Activity')]]//following-sibling::div//button")
    LOCATION_INPUT = (By.XPATH, "//label[.//span[contains(text(), 'Location')]]//following::input[@placeholder='Select Location'][1]")
    QUANTITY_INPUT = (By.XPATH, "//input[@placeholder='Enter Quantity']")
    UNIT_DROPDOWN = (By.XPATH, "//label[.//span[contains(text(), 'Unit of Measurement')]]//following-sibling::div//button")
    SUBCONTRACTOR_INPUT = (By.XPATH, "//input[@placeholder='Enter sub contractor name']")
    CHECKPOINT_DROPDOWN = (By.XPATH, "//label[.//span[contains(text(), 'Inspection Checkpoint')]]//following-sibling::div//button")
    CHECKLIST_DROPDOWN = (By.XPATH, "//label[.//span[contains(text(), 'Inspection Checklist')]]//following-sibling::div//button")
    
    # Page 2 - Question sections (collapsed/expandable)
    QUESTION_SECTION = (By.CSS_SELECTOR, "div[data-scope='collapsible']")
    COLLAPSE_ALL_BUTTON = (By.XPATH, "//button[.//svg[contains(@class, 'lucide-square-minus')]]")
    EXPAND_BUTTON = (By.CSS_SELECTOR, "button.collapsible__trigger")
    
    # Success messages
    SUCCESS_TOAST = (By.XPATH, "//*[contains(text(),'successfully') or contains(text(),'Success')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def wait_for_form_visible(self):
        """Wait for inspection checklist form to be visible."""
        print("[INFO] Waiting for Inspection Checklist form...")
        self.wait.until(EC.visibility_of_element_located(self.FORM_TITLE))
        print("[SUCCESS] Inspection Checklist form is visible.")

    def is_on_page_1(self):
        """Check if we are on page 1."""
        try:
            self.driver.find_element(*self.PAGE_1_INDICATOR)
            return True
        except:
            return False

    def is_on_page_2(self):
        """Check if we are on page 2."""
        try:
            self.driver.find_element(*self.PAGE_2_INDICATOR)
            return True
        except:
            return False

    def get_question_by_number(self, question_number):
        """Get question section by its number (1-12)."""
        xpath = f"(//div[@data-scope='collapsible'])[{question_number}]"
        return (By.XPATH, xpath)

    def get_observation_input_for_question(self, question_number):
        """Get observation/measured value input for a specific question."""
        xpath = f"(//label[contains(text(), 'Observation/Measured Value')])[{question_number}]/following-sibling::input"
        return (By.XPATH, xpath)

    def get_camera_button_for_question(self, question_number):
        """Get camera button for a specific question."""
        xpath = f"(//div[contains(@class, 'lucide-camera')])[{question_number}]"
        return (By.XPATH, xpath)

    def expand_question_section(self, question_number):
        """Expand a specific question section if collapsed."""
        print(f"[ACTION] Expanding question {question_number}...")
        question_section = self.get_question_by_number(question_number)
        
        try:
            # Check if already expanded
            section_element = self.wait.until(EC.presence_of_element_located(question_section))
            state = section_element.get_attribute("data-state")
            
            if state == "closed":
                # Click the expand button within this section
                expand_button = section_element.find_element(By.CSS_SELECTOR, "button[data-part='trigger']")
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", expand_button)
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].click();", expand_button)
                time.sleep(0.3)
                print(f"[SUCCESS] Question {question_number} expanded.")
            else:
                print(f"[INFO] Question {question_number} already expanded.")
        except Exception as e:
            print(f"[ERROR] Failed to expand question {question_number}: {str(e)}")

    def fill_observation_for_question(self, question_number, observation_text):
        """Fill observation/measured value for a specific question."""
        print(f"[ACTION] Filling observation for question {question_number}...")
        
        # Expand the section first
        self.expand_question_section(question_number)
        
        # Find and fill the input
        input_locator = self.get_observation_input_for_question(question_number)
        
        try:
            input_element = self.wait.until(EC.visibility_of_element_located(input_locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", input_element)
            time.sleep(0.2)
            
            input_element.clear()
            input_element.send_keys(observation_text)
            input_element.send_keys(Keys.TAB)
            
            print(f"[SUCCESS] Filled observation for question {question_number}: {observation_text}")
        except Exception as e:
            print(f"[ERROR] Failed to fill observation for question {question_number}: {str(e)}")

    def fill_all_questions_on_page_2(self, observations=None):
        """Fill all 12 questions on page 2 with observations."""
        print("=== FILLING ALL QUESTIONS ON PAGE 2 ===")
        
        # Default observations if none provided
        if observations is None:
            observations = [
                "Fasteners installed correctly with torque marks",
                "Drive post installed within tolerance, heights maintained",
                "Slew drive seat installed at ±0° angle",
                "Post seat installed correctly, grounding cable in place",
                "Slew drives aligned properly, motor facing south",
                "Correct torque tube installed, alignment within tolerance",
                "Purlins secured with torque marks, gaskets in place",
                "Transmission shaft assembly installed correctly",
                "Tube covers placed on both ends",
                "Grounding cables installed at both ends and control box",
                "AI Controller box accessories installed, cables properly routed",
                "Communication box and wind sensor properly installed"
            ]
        
        # Ensure we have 12 observations
        while len(observations) < 12:
            observations.append("Verified as per installation manual")
        
        # Fill each question
        for i in range(1, 13):
            self.fill_observation_for_question(i, observations[i-1])
            time.sleep(0.2)  # Small delay between questions
        
        print("=== ALL QUESTIONS FILLED ===")

    def collapse_all_questions(self):
        """Click the collapse all button to minimize all sections."""
        print("[ACTION] Collapsing all question sections...")
        try:
            collapse_btn = self.wait.until(EC.element_to_be_clickable(self.COLLAPSE_ALL_BUTTON))
            self.driver.execute_script("arguments[0].click();", collapse_btn)
            time.sleep(0.5)
            print("[SUCCESS] All questions collapsed.")
        except Exception as e:
            print(f"[ERROR] Failed to collapse questions: {str(e)}")

    def click_proceed_from_page_1(self):
        """Click proceed button on page 1."""
        print("[ACTION] Clicking Proceed from page 1...")
        try:
            proceed_btn = self.wait.until(EC.element_to_be_clickable(self.PROCEED_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", proceed_btn)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", proceed_btn)
            time.sleep(0.5)
            print("[SUCCESS] Clicked Proceed - moved to page 2.")
        except Exception as e:
            print(f"[ERROR] Failed to click Proceed: {str(e)}")

    def submit_checklist_form(self):
        """Submit the inspection checklist form."""
        print("[ACTION] Submitting inspection checklist form...")
        try:
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.3)
            
            submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", submit_btn)
            
            # Wait for success message
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_TOAST))
            print("[SUCCESS] Inspection checklist submitted successfully!")
            
        except Exception as e:
            print(f"[ERROR] Failed to submit form: {str(e)}")
            raise

    def complete_inspection_checklist(self, observations=None):
        """Complete the entire inspection checklist workflow."""
        print("\n=== STARTING INSPECTION CHECKLIST ===")
        
        # Wait for form to load
        self.wait_for_form_visible()
        
        # Check current page
        if self.is_on_page_1():
            print("[INFO] Currently on page 1, clicking Proceed...")
            self.click_proceed_from_page_1()
        
        # Verify we're on page 2
        if not self.is_on_page_2():
            raise Exception("Failed to navigate to page 2")
        
        print("[INFO] Now on page 2 - Filling questions...")
        
        # Fill all questions
        self.fill_all_questions_on_page_2(observations)
        
        # Optionally collapse sections for cleaner view
        # self.collapse_all_questions()
        
        # Submit the form
        self.submit_checklist_form()
        
        print("=== INSPECTION CHECKLIST COMPLETED ===\n")
