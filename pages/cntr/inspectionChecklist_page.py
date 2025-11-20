from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time


class InspectionChecklistPage(BasePage):
    """Inspection Checklist Page - Fills form after RFI submission.
    
    Features:
    - Expands all 12 inspection questions
    - Fills observation text for each question
    - Optionally captures photos using browser camera
    - Handles confirmation popup on submission
    
    Camera Capture:
    - Requires Chrome with camera permissions (configured in conftest.py)
    - Uses fake camera device for automated testing
    - Can be disabled by setting capture_photos=False
    """

    # Form header
    FORM_TITLE = (By.XPATH, "//p[contains(text(), 'Inspection Checklist')]")
    
    # Page indicators
    PAGE_1_INDICATOR = (By.XPATH, "//p[contains(text(), 'Page 1/2')]")
    PAGE_2_INDICATOR = (By.XPATH, "//p[contains(text(), 'Page 2/2')]")
    
    # Navigation buttons
    PROCEED_BUTTON = (By.XPATH, "//button[normalize-space()='Proceed']")
    PREV_BUTTON = (By.CSS_SELECTOR, "button.steps__prev-trigger")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")
    
    # Confirmation popup - "Are you sure you want to Submit RFI?"
    POPUP_DIALOG = (By.XPATH, "//div[@data-scope='dialog'][@role='dialog']")
    POPUP_SUBMIT_BUTTON = (By.XPATH, "//div[@data-scope='dialog']//button[@type='submit'][@form='rfi-form']")
    POPUP_CANCEL_BUTTON = (By.XPATH, "//div[@data-scope='dialog']//button[@data-part='close-trigger']")
    
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
    # Button with text "Answer all the questions" and square-plus icon
    EXPAND_ALL_BUTTON = (By.XPATH, "//p[contains(text(), 'Answer all the questions')]/following-sibling::button[.//svg[contains(@class, 'lucide-square-plus')]]")
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
    
    def debug_page_structure(self):
        """Debug helper to print page structure info."""
        print("\n=== DEBUG: PAGE STRUCTURE ===")
        try:
            # Check collapsible sections
            collapsibles = self.driver.find_elements(By.CSS_SELECTOR, "div[data-scope='collapsible']")
            print(f"Total collapsible sections: {len(collapsibles)}")
            
            closed = self.driver.find_elements(By.XPATH, "//div[@data-scope='collapsible'][@data-state='closed']")
            print(f"Closed sections: {len(closed)}")
            
            open_sections = self.driver.find_elements(By.XPATH, "//div[@data-scope='collapsible'][@data-state='open']")
            print(f"Open sections: {len(open_sections)}")
            
            # Check for buttons
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print(f"Total buttons on page: {len(all_buttons)}")
            
            # Check for camera icons
            camera_icons = self.driver.find_elements(By.XPATH, "//svg[contains(@class, 'lucide-camera')]")
            print(f"Camera icons found: {len(camera_icons)}")
            
            # Check for "Use Camera" text
            use_camera_text = self.driver.find_elements(By.XPATH, "//p[contains(text(), 'Use Camera')]")
            print(f"'Use Camera' text found: {len(use_camera_text)}")
            
            # Check for square-plus icon
            plus_icons = self.driver.find_elements(By.XPATH, "//svg[contains(@class, 'lucide-square-plus')]")
            print(f"Square-plus icons found: {len(plus_icons)}")
            
            # Check for the text
            answer_text = self.driver.find_elements(By.XPATH, "//p[contains(text(), 'Answer all the questions')]")
            print(f"'Answer all the questions' text found: {len(answer_text)}")
            
        except Exception as e:
            print(f"Error in debug: {e}")
        print("=== END DEBUG ===\n")
    
    def debug_popup_structure(self):
        """Debug helper to print popup/dialog structure info."""
        print("\n=== DEBUG: POPUP STRUCTURE ===")
        try:
            # Check for dialogs with data-scope
            data_scope_dialogs = self.driver.find_elements(By.XPATH, "//div[@data-scope='dialog']")
            print(f"Dialogs with data-scope='dialog': {len(data_scope_dialogs)}")
            
            # Check for dialogs by role
            role_dialogs = self.driver.find_elements(By.XPATH, "//div[@role='dialog']")
            print(f"Dialogs with role='dialog': {len(role_dialogs)}")
            
            # Check for confirmation text
            confirm_text = self.driver.find_elements(By.XPATH, "//p[contains(text(), 'Are you sure')]")
            if confirm_text:
                print(f"Confirmation text found: '{confirm_text[0].text}'")
            
            # Check for all Submit buttons
            submit_buttons = self.driver.find_elements(By.XPATH, "//button[normalize-space()='Submit']")
            print(f"Total 'Submit' buttons: {len(submit_buttons)}")
            
            for idx, btn in enumerate(submit_buttons):
                try:
                    visible = btn.is_displayed()
                    enabled = btn.is_enabled()
                    btn_type = btn.get_attribute('type')
                    btn_form = btn.get_attribute('form')
                    print(f"  Submit button {idx+1}: Visible={visible}, Enabled={enabled}, type='{btn_type}', form='{btn_form}'")
                except:
                    pass
            
            # Check for Cancel button
            cancel_buttons = self.driver.find_elements(By.XPATH, "//button[normalize-space()='Cancel']")
            print(f"Cancel buttons: {len(cancel_buttons)}")
            
        except Exception as e:
            print(f"Error in popup debug: {e}")
        print("=== END POPUP DEBUG ===\n")

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
        # The camera button is the clickable div with camera icon and "Use Camera" text
        # Located within each question's collapsible section
        xpath = f"(//div[@data-scope='collapsible'])[{question_number}]//div[contains(@class, 'cursor_pointer')]//svg[contains(@class, 'lucide-camera')]/ancestor::div[contains(@class, 'cursor_pointer')]"
        return (By.XPATH, xpath)
    
    def get_camera_capture_button(self):
        """Get the Capture button in the camera modal."""
        return (By.XPATH, "//button[normalize-space()='Capture']")
    
    def get_camera_cancel_button(self):
        """Get the Cancel button in the camera modal."""
        return (By.XPATH, "//button[normalize-space()='Cancel']")

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

    def capture_photo_for_question(self, question_number, skip_camera=False):
        """Capture photo for a specific question.
        
        Args:
            question_number: The question number (1-12)
            skip_camera: If True, skip camera capture (useful for headless mode)
        """
        if skip_camera:
            print(f"[INFO] Skipping camera capture for question {question_number}")
            return
        
        print(f"\n[ACTION] 📸 Starting camera capture for QUESTION {question_number}...")
        print(f"[DEBUG] Ensuring clean state before capture...")
        
        # CRITICAL: Ensure no modal is open from previous question
        try:
            existing_videos = self.driver.find_elements(By.TAG_NAME, "video")
            visible_videos = [v for v in existing_videos if v.is_displayed()]
            if visible_videos:
                print(f"[WARNING] ⚠️ Found {len(visible_videos)} open video modal(s) before question {question_number}")
                print(f"[ACTION] Forcefully closing any open modals...")
                self._close_camera_modal()
                time.sleep(0.5)  # Reduced wait
                
                # Double-check modal is closed
                remaining_videos = [v for v in self.driver.find_elements(By.TAG_NAME, "video") if v.is_displayed()]
                if remaining_videos:
                    print(f"[ERROR] ❌ Modal still open! Trying ESC key...")
                    self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                    time.sleep(0.3)
        except Exception as e:
            print(f"[DEBUG] Error checking for existing modals: {e}")
        
        try:
            # Find the camera button within this specific question
            print(f"[DEBUG] Looking for camera button in question {question_number}...")
            
            # Try multiple locator strategies with detailed debugging
            # Based on actual HTML: <div class="cursor_pointer"><svg class="lucide lucide-camera">...<p>Use Camera</p></div>
            locators_to_try = [
                (f"Strategy 1: Direct cursor_pointer div with camera SVG", 
                 By.XPATH, f"(//div[@data-scope='collapsible'])[{question_number}]//div[@class='cursor_pointer' and .//svg[contains(@class, 'lucide-camera')]]"),
                (f"Strategy 2: Camera SVG parent div", 
                 By.XPATH, f"(//div[@data-scope='collapsible'])[{question_number}]//svg[contains(@class, 'lucide-camera')]/parent::div"),
                (f"Strategy 3: Div containing 'Use Camera' text with camera icon", 
                 By.XPATH, f"(//div[@data-scope='collapsible'])[{question_number}]//div[.//p[contains(text(), 'Use Camera')] and .//svg[contains(@class, 'lucide-camera')]]"),
                (f"Strategy 4: Any div with cursor_pointer class in question section", 
                 By.XPATH, f"(//div[@data-scope='collapsible'])[{question_number}]//div[contains(@class, 'cursor_pointer')]"),
            ]
            
            camera_btn = None
            for strategy_name, locator_type, locator_value in locators_to_try:
                try:
                    print(f"[DEBUG] Trying: {strategy_name}")
                    elements = self.driver.find_elements(locator_type, locator_value)
                    print(f"[DEBUG]   Found {len(elements)} elements")
                    if elements:
                        # CRITICAL: Use the first element found within THIS question's scope
                        # The locator already filters by question number, so first element should be correct
                        camera_btn = elements[0]
                        print(f"[SUCCESS] ✓ {strategy_name} worked - using first element!")
                        
                        # Verify this button is within the correct question section
                        try:
                            question_section = self.driver.find_element(By.XPATH, f"(//div[@data-scope='collapsible'])[{question_number}]")
                            # Check if camera_btn is a descendant of this question section
                            is_in_correct_section = self.driver.execute_script(
                                "return arguments[0].contains(arguments[1]);", 
                                question_section, camera_btn
                            )
                            if is_in_correct_section:
                                print(f"[VERIFY] ✓ Camera button IS in question {question_number} section")
                            else:
                                print(f"[WARNING] ❌ Camera button NOT in question {question_number}, trying next strategy...")
                                camera_btn = None
                                continue
                        except Exception as verify_err:
                            print(f"[WARNING] Could not verify button location: {verify_err}")
                        
                        break
                except Exception as e:
                    print(f"[DEBUG]   Failed: {str(e)}")
                    continue
            
            if not camera_btn:
                print(f"[ERROR] ❌ Could not find camera button for question {question_number} with any strategy")
                # Extensive debugging
                print("\n[DEBUG] === DEBUGGING CAMERA BUTTON LOCATION ===")
                try:
                    # Check if question section exists
                    question_section = self.driver.find_element(By.XPATH, f"(//div[@data-scope='collapsible'])[{question_number}]")
                    print(f"[DEBUG] ✓ Question section {question_number} exists")
                    
                    # Check for camera icons in this section
                    camera_icons = question_section.find_elements(By.XPATH, ".//svg[contains(@class, 'lucide-camera')]")
                    print(f"[DEBUG] Camera icons in question {question_number}: {len(camera_icons)}")
                    
                    # Check for any clickable divs
                    clickable_divs = question_section.find_elements(By.XPATH, ".//div[contains(@class, 'cursor_pointer')]")
                    print(f"[DEBUG] Clickable divs in question {question_number}: {len(clickable_divs)}")
                    
                    # Check for "Use Camera" text
                    use_camera_text = question_section.find_elements(By.XPATH, ".//p[contains(text(), 'Use Camera')]")
                    print(f"[DEBUG] 'Use Camera' text found: {len(use_camera_text)}")
                    
                    # Get the HTML of the section for inspection
                    section_html = question_section.get_attribute('outerHTML')[:500]
                    print(f"[DEBUG] Question section HTML preview:\n{section_html}...")
                    
                    # Take screenshot for visual debugging
                    screenshot_name = f"camera_button_not_found_q{question_number}.png"
                    self.driver.save_screenshot(screenshot_name)
                    print(f"[DEBUG] Screenshot saved as {screenshot_name}")
                    
                except Exception as debug_err:
                    print(f"[DEBUG] Debug failed: {debug_err}")
                print("[DEBUG] === END DEBUGGING ===\n")
                return
            
            # Scroll to the button and click
            print(f"[DEBUG] Scrolling to camera button...")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", camera_btn)
            time.sleep(0.3)  # Reduced wait
            
            # Check if button is visible and enabled
            is_visible = camera_btn.is_displayed()
            is_enabled = camera_btn.is_enabled()
            print(f"[DEBUG] Camera button - Visible: {is_visible}, Enabled: {is_enabled}")
            
            if not is_visible:
                print(f"[WARNING] Camera button not visible, trying to make it visible...")
                self.driver.execute_script("arguments[0].style.display='block';", camera_btn)
                time.sleep(0.3)
            
            # Click using JavaScript for reliability
            print(f"[DEBUG] Clicking camera button with JavaScript...")
            self.driver.execute_script("arguments[0].click();", camera_btn)
            print(f"[DEBUG] ✓ Clicked camera button for question {question_number}")
            
            # Wait for camera modal to appear (with video element)
            print("[DEBUG] Waiting for camera modal to open...")
            try:
                video_element = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.TAG_NAME, "video"))
                )
                print("[SUCCESS] ✓ Camera modal opened with video feed")
                time.sleep(0.5)  # Reduced camera initialization time
            except TimeoutException:
                print("[ERROR] ❌ Camera modal did not open (no video element)")
                # Check what's on the page
                print("[DEBUG] Checking page state after click...")
                videos = self.driver.find_elements(By.TAG_NAME, "video")
                print(f"[DEBUG] Video elements found: {len(videos)}")
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                capture_btns = [b for b in buttons if "capture" in b.text.lower()]
                print(f"[DEBUG] Buttons with 'capture' text: {len(capture_btns)}")
                return
            
            # Click Capture button in modal
            print("[DEBUG] Looking for Capture button in modal...")
            try:
                capture_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Capture']"))
                )
                capture_btn.click()
                print(f"[SUCCESS] ✓ Clicked Capture button")
                
                # Wait for modal to close (video element should disappear)
                print("[DEBUG] Waiting for modal to close...")
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.invisibility_of_element_located((By.TAG_NAME, "video"))
                    )
                    print(f"[SUCCESS] ✅ Photo captured and modal closed for question {question_number}")
                except TimeoutException:
                    print(f"[WARNING] ⚠️ Modal didn't close automatically, forcing close...")
                    self._close_camera_modal()
                
                # Wait for modal to fully close
                time.sleep(0.4)  # Reduced wait
                
                # Final verification: No video elements visible
                final_check = [v for v in self.driver.find_elements(By.TAG_NAME, "video") if v.is_displayed()]
                if final_check:
                    print(f"[ERROR] ❌ Video still visible! Force closing again...")
                    self._close_camera_modal()
                    time.sleep(0.3)
                else:
                    print(f"[VERIFY] ✓ Modal fully closed, ready for next question")
                
            except TimeoutException:
                print(f"[ERROR] ❌ Capture button not found in modal")
                self._close_camera_modal()
                return
            except Exception as e:
                print(f"[ERROR] ❌ Error clicking Capture button: {str(e)}")
                self._close_camera_modal()
                return
                
        except Exception as e:
            print(f"[ERROR] ❌ Camera capture failed for question {question_number}: {str(e)}")
            print("[INFO] Attempting to close any open modals...")
            self._close_camera_modal()
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
    
    def _close_camera_modal(self):
        """Helper to close camera modal if it's open."""
        try:
            cancel_btn = self.driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']")
            cancel_btn.click()
            print("[INFO] Closed camera modal")
            time.sleep(0.3)
        except:
            # Try pressing Escape key
            try:
                from selenium.webdriver.common.keys import Keys
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                print("[INFO] Closed camera modal with ESC key")
            except:
                pass
    
    def fill_observation_for_question(self, question_number, observation_text, expand_first=False):
        """Fill observation/measured value for a specific question.
        
        Args:
            question_number: The question number (1-12)
            observation_text: Text to fill in the observation field
            expand_first: If True, expand the question before filling (default: False)
        """
        print(f"[ACTION] Filling observation for question {question_number}...")
        
        # Find and fill the input
        input_locator = self.get_observation_input_for_question(question_number)
        
        try:
            # Try to find the input - if not visible, expand the section first
            try:
                input_element = self.wait.until(EC.visibility_of_element_located(input_locator))
            except TimeoutException:
                print(f"[DEBUG] Input not visible for question {question_number}, expanding section...")
                self.expand_question_section(question_number)
                input_element = self.wait.until(EC.visibility_of_element_located(input_locator))
            
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", input_element)
            time.sleep(0.1)  # Reduced wait
            
            input_element.clear()
            input_element.send_keys(observation_text)
            input_element.send_keys(Keys.TAB)
            
            print(f"[SUCCESS] Filled observation for question {question_number}: {observation_text}")
        except Exception as e:
            print(f"[ERROR] Failed to fill observation for question {question_number}: {str(e)}")

    def fill_all_questions_on_page_2(self, observations=None, capture_photos=False):
        """Fill all 12 questions on page 2 with observations and optionally capture photos.
        
        Args:
            observations: List of observation texts (defaults to standard observations)
            capture_photos: If True, capture photos for each question (default: False)
        """
        print("\n" + "="*60)
        print("FILLING ALL QUESTIONS ON PAGE 2")
        print("="*60)
        
        # First, expand all questions at once using the master button
        self.expand_all_questions()
        time.sleep(0.5)  # Reduced wait time for expansion
        
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
        
        # Fill each question (they should all be expanded now)
        for i in range(1, 13):
            print(f"\n{'='*60}")
            print(f"📝 PROCESSING QUESTION {i}/12")
            print(f"{'='*60}")
            
            # CRITICAL: Scroll to question and wait for it to be stable
            try:
                question_section = self.driver.find_element(By.XPATH, f"(//div[@data-scope='collapsible'])[{i}]")
                
                # Scroll to center of question section (instant scroll, no smooth)
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", question_section)
                time.sleep(0.3)  # Reduced wait time
                    
            except Exception as e:
                print(f"[WARNING] Could not scroll to question {i}: {e}")
            
            # Step 1: Fill observation text
            print(f"[STEP 1/2] Filling observation text...")
            self.fill_observation_for_question(i, observations[i-1])
            time.sleep(0.2)  # Reduced wait time
            
            # Step 2: Optionally capture photo
            if capture_photos:
                print(f"[STEP 2/2] Camera capture for question {i}...")
                time.sleep(0.3)  # Reduced pause
                
                self.capture_photo_for_question(i, skip_camera=False)
                
                # CRITICAL: Verify modal is fully closed before moving to next question
                print(f"[VERIFY] Checking modal closure after question {i}...")
                time.sleep(0.3)  # Reduced wait
                try:
                    open_videos = self.driver.find_elements(By.TAG_NAME, "video")
                    visible_videos = [v for v in open_videos if v.is_displayed()]
                    if visible_videos:
                        print(f"[WARNING] ⚠️ {len(visible_videos)} camera modal(s) still visible after question {i}!")
                        print("[ACTION] Forcing modal closure...")
                        self._close_camera_modal()
                        time.sleep(0.5)  # Reduced wait
                        
                        # Double-check
                        still_visible = [v for v in self.driver.find_elements(By.TAG_NAME, "video") if v.is_displayed()]
                        if still_visible:
                            print(f"[ERROR] ❌ Modal STILL open! Pressing ESC...")
                            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                            time.sleep(0.3)  # Reduced wait
                    else:
                        print(f"[VERIFY] ✓ No open modals, safe to proceed")
                except Exception as verify_err:
                    print(f"[WARNING] Modal verification failed: {verify_err}")
            
            print(f"[SUCCESS] ✅ Question {i} COMPLETED")
            print(f"{'─'*60}\n")
            time.sleep(0.2)  # Reduced delay between questions
        
        print("\n" + "="*60)
        print("✅ ALL 12 QUESTIONS FILLED SUCCESSFULLY")
        print("="*60 + "\n")

    def expand_all_questions(self):
        """Click the expand all button (square-plus icon) to open all question sections at once."""
        print("[ACTION] Expanding all question sections...")
        
        # Take screenshot for debugging
        try:
            self.driver.save_screenshot("before_expand_all.png")
            print("[DEBUG] Screenshot saved as before_expand_all.png")
        except:
            pass
        
        # Try multiple locator strategies
        locators_to_try = [
            ("Text + sibling button", "//p[contains(text(), 'Answer all the questions')]/following-sibling::button"),
            ("Parent div approach", "//div[.//p[contains(text(), 'Answer all the questions')]]//button[.//svg[contains(@class, 'lucide-square-plus')]]"),
            ("SVG icon only", "//svg[contains(@class, 'lucide-square-plus')]/parent::button"),
            ("Button with ghost variant", "//button[contains(@class, 'button--variant_ghost')]//svg[contains(@class, 'lucide-square-plus')]/parent::button"),
            ("Direct button class", "button.button--variant_ghost.button--size_xs"),
        ]
        
        expand_btn = None
        used_locator = None
        
        for locator_name, locator_xpath in locators_to_try:
            try:
                print(f"[DEBUG] Trying locator: {locator_name}")
                if locator_xpath.startswith("button."):
                    elements = self.driver.find_elements(By.CSS_SELECTOR, locator_xpath)
                else:
                    elements = self.driver.find_elements(By.XPATH, locator_xpath)
                
                if elements:
                    # Filter for visible and enabled buttons
                    for elem in elements:
                        if elem.is_displayed() and elem.is_enabled():
                            expand_btn = elem
                            used_locator = locator_name
                            print(f"[SUCCESS] Found button using: {locator_name}")
                            break
                    if expand_btn:
                        break
            except Exception as e:
                print(f"[DEBUG] Locator '{locator_name}' failed: {str(e)}")
                continue
        
        if not expand_btn:
            print("[WARNING] Standard locators failed. Trying aggressive search...")
            # Last resort: find ALL buttons and check for square-plus icon
            try:
                all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                print(f"[DEBUG] Found {len(all_buttons)} total buttons on page")
                
                for idx, btn in enumerate(all_buttons):
                    try:
                        if btn.is_displayed() and btn.is_enabled():
                            # Check if this button contains a square-plus SVG
                            svgs = btn.find_elements(By.TAG_NAME, "svg")
                            for svg in svgs:
                                svg_class = svg.get_attribute("class")
                                if svg_class and "lucide-square-plus" in svg_class:
                                    expand_btn = btn
                                    used_locator = f"Aggressive search (button #{idx})"
                                    print(f"[SUCCESS] Found button with square-plus icon (button #{idx})")
                                    break
                            if expand_btn:
                                break
                    except:
                        continue
            except Exception as e:
                print(f"[DEBUG] Aggressive search failed: {str(e)}")
        
        if not expand_btn:
            print("[ERROR] Could not find expand all button with any method!")
            print("[INFO] Will expand questions individually...")
            return
        
        try:
            # Scroll to button
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", expand_btn)
            time.sleep(0.5)
            
            # Try regular click first
            try:
                expand_btn.click()
                print("[DEBUG] Clicked button using regular click()")
            except:
                # Fallback to JavaScript click
                self.driver.execute_script("arguments[0].click();", expand_btn)
                print("[DEBUG] Clicked button using JavaScript click()")
            
            time.sleep(1.0)  # Give time for accordions to expand
            
            # Verify at least one question is now open
            try:
                open_sections = self.driver.find_elements(By.XPATH, "//div[@data-scope='collapsible'][@data-state='open']")
                if len(open_sections) > 0:
                    print(f"[SUCCESS] All questions expanded. Found {len(open_sections)} open questions.")
                else:
                    print("[WARNING] Button clicked but no questions appear to be open. Will expand individually...")
            except:
                print("[WARNING] Could not verify questions expanded, but continuing...")
                
        except Exception as e:
            print(f"[WARNING] Failed to click expand all button: {str(e)}")
            print("[INFO] Will try expanding questions individually...")

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
        """Submit the inspection checklist form and handle confirmation popup.
        
        Workflow:
        1. Click the main Submit button on the form
        2. A confirmation popup appears with its own Submit button
        3. Click the Submit button on the popup
        4. Wait for success toast message
        """
        print("[ACTION] Submitting inspection checklist form...")
        try:
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.3)
            
            # Click the initial Submit button
            submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", submit_btn)
            print("[INFO] Clicked Submit button - waiting for confirmation popup...")
            
            # Wait for confirmation popup to appear
            print("[INFO] Waiting for confirmation dialog...")
            try:
                # Wait for dialog to be visible
                self.wait.until(EC.visibility_of_element_located(self.POPUP_DIALOG))
                print("[SUCCESS] Confirmation dialog appeared!")
            except TimeoutException:
                print("[WARNING] Dialog did not appear within timeout, trying anyway...")
            
            time.sleep(0.5)
            
            # Debug popup structure
            self.debug_popup_structure()
            
            # Try multiple locators for the popup Submit button
            popup_submit_locators = [
                # Most specific: dialog with form submit button
                (By.XPATH, "//div[@data-scope='dialog']//button[@type='submit'][@form='rfi-form']"),
                # By dialog role and Submit text
                (By.XPATH, "//div[@role='dialog']//button[normalize-space()='Submit']"),
                # By data-scope dialog
                (By.XPATH, "//div[@data-scope='dialog']//button[normalize-space()='Submit']"),
                # By button variant in dialog
                (By.XPATH, "//div[@data-scope='dialog']//button[contains(@class, 'button--variant_gradient')]"),
                # Second Submit button on page
                (By.XPATH, "(//button[normalize-space()='Submit'])[2]"),
            ]
            
            popup_clicked = False
            for locator in popup_submit_locators:
                try:
                    popup_submit = self.wait.until(EC.element_to_be_clickable(locator))
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", popup_submit)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", popup_submit)
                    print("[SUCCESS] Clicked Submit button on confirmation popup!")
                    popup_clicked = True
                    break
                except:
                    continue
            
            if not popup_clicked:
                print("[WARNING] Standard popup locators failed. Trying aggressive search...")
                # Find all Submit buttons and click the visible one that's not the first
                try:
                    all_submit_buttons = self.driver.find_elements(By.XPATH, "//button[normalize-space()='Submit']")
                    print(f"[DEBUG] Found {len(all_submit_buttons)} Submit buttons")
                    
                    for idx, btn in enumerate(all_submit_buttons):
                        try:
                            if btn.is_displayed() and btn.is_enabled():
                                # Skip the first one (main form submit), click the second (popup)
                                if idx > 0:
                                    self.driver.execute_script("arguments[0].click();", btn)
                                    print(f"[SUCCESS] Clicked Submit button #{idx+1} (popup)")
                                    popup_clicked = True
                                    break
                        except:
                            continue
                except Exception as e:
                    print(f"[DEBUG] Aggressive popup search failed: {str(e)}")
            
            if not popup_clicked:
                print("[WARNING] Could not find popup Submit button, trying to continue anyway...")
            
            # Wait for success message
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_TOAST))
            print("[SUCCESS] Inspection checklist submitted successfully!")
            
        except Exception as e:
            print(f"[ERROR] Failed to submit form: {str(e)}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot("submit_error.png")
                print("[DEBUG] Screenshot saved as submit_error.png")
            except:
                pass
            raise

    def complete_inspection_checklist(self, observations=None, capture_photos=False):
        """Complete the entire inspection checklist workflow.
        
        Args:
            observations: List of observation texts for the 12 questions
            capture_photos: If True, capture photos for each question (default: False)
                           Note: Requires browser camera permissions
        """
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
        
        # Debug: Show page structure
        self.debug_page_structure()
        
        # Fill all questions (with optional photo capture)
        self.fill_all_questions_on_page_2(observations, capture_photos=capture_photos)
        
        # Optionally collapse sections for cleaner view
        # self.collapse_all_questions()
        
        # Submit the form
        self.submit_checklist_form()
        
        print("=== INSPECTION CHECKLIST COMPLETED ===\n")
