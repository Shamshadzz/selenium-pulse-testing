import pytest
from selenium.webdriver.common.by import By
from pages.cntr.createRfi_page import CreateRfiPage
from pages.cntr.inspectionChecklist_page import InspectionChecklistPage
import time


@pytest.mark.rfi
@pytest.mark.smoke
class TestCreateRfi:
    def test_create_rfi_complete(self, contractor_driver, base_url):
        """Test: Fill all RFI fields, submit, and complete inspection checklist."""
        try:
            # Step 1: Fill RFI form (Page 1) and click Proceed
            print("\n🔷 STEP 1: Filling RFI form...")
            rfi_page = CreateRfiPage(contractor_driver)
            rfi_page.navigate()
            rfi_page.create_rfi()

            print("\n✅ RFI form filled and Proceed clicked - now on Inspection Checklist page.")
            
            # Step 2: Wait for transition to Inspection Checklist page
            time.sleep(2)
            
            # Debug: Check current page state
            print("\n🔍 DEBUG: Checking page state...")
            try:
                page_indicator = contractor_driver.find_element(By.XPATH, "//p[contains(text(), 'Page')]")
                print(f"  Current page: {page_indicator.text}")
            except:
                print("  Could not find page indicator")
            
            # Step 3: Complete Inspection Checklist and submit
            print("\n🔷 STEP 2: Starting Inspection Checklist workflow...")
            checklist_page = InspectionChecklistPage(contractor_driver)
            # Set capture_photos=True to enable camera capture for each question
            # Set capture_photos=False to skip camera (faster testing)
            checklist_page.complete_inspection_checklist(capture_photos=True)
            
            # Verify final success
            assert checklist_page.is_element_visible(InspectionChecklistPage.SUCCESS_TOAST), \
                "Inspection checklist not submitted or success message missing."
            
            print("\n✅ Complete RFI workflow finished (RFI + Inspection Checklist).")
            
        except Exception as e:
            print(f"\n❌ TEST FAILED: {str(e)}")
            # Take screenshot on failure
            try:
                contractor_driver.save_screenshot("test_failure.png")
                print("📸 Screenshot saved as test_failure.png")
            except:
                pass
            raise
    def test_contractor_incharge_workflow(self, contractor_incharge_driver, base_url):
        """
        Test Workflow for Contractor Incharge:
        1. Login (handled by fixture)
        2. Create RFI -> Submit
        3. Inspection Checklist -> Submit -> Confirm
        """
        driver = contractor_incharge_driver
        print("\n🔷 START: Contractor Incharge Workflow")
        
        try:
            # Step 1: Create RFI
            print("\n🔷 STEP 1: Filling RFI form...")
            rfi_page = CreateRfiPage(driver)
            rfi_page.navigate()
            rfi_page.create_rfi()
            
            print("\n✅ RFI form submitted. Transitioning to Inspection Checklist...")
            time.sleep(2) # Wait for transition
            
            # Step 2: Inspection Checklist
            print("\n🔷 STEP 2: Filling Inspection Checklist...")
            checklist_page = InspectionChecklistPage(driver)
            
            # Verify we are on the checklist page
            assert checklist_page.is_element_visible(InspectionChecklistPage.FORM_TITLE), "Not on Inspection Checklist page"
            
            # Complete checklist with camera (optional, set to False for speed if needed)
            checklist_page.complete_inspection_checklist(capture_photos=True)
            
            # Verify final success
            assert checklist_page.is_element_visible(InspectionChecklistPage.SUCCESS_TOAST), \
                "Workflow failed: Success message not found."
                
            print("\n✅ Contractor Incharge Workflow COMPLETED successfully.")
            
        except Exception as e:
            print(f"\n❌ WORKFLOW FAILED: {str(e)}")
            try:
                driver.save_screenshot("errors/cntr_incharge_failure.png")
                print("📸 Screenshot saved as errors/cntr_incharge_failure.png")
            except:
                pass
            raise
