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
