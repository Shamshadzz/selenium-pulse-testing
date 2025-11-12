import pytest
from pages.cntr.createRfi_page import CreateRfiPage
from pages.cntr.inspectionChecklist_page import InspectionChecklistPage
import time


@pytest.mark.rfi
@pytest.mark.smoke
class TestCreateRfi:
    def test_create_rfi_complete(self, contractor_driver, base_url):
        """Test: Fill all RFI fields, submit, and complete inspection checklist."""
        # Step 1: Create RFI
        rfi_page = CreateRfiPage(contractor_driver)
        rfi_page.navigate()
        rfi_page.create_rfi()

        assert rfi_page.is_element_visible(CreateRfiPage.SUCCESS_TOAST), \
            "RFI not created or success message missing."

        print("\n✅ RFI form filled and submitted successfully.")
        
        # Step 2: Wait for success toast to disappear and form to transition
        time.sleep(2)
        
        # Step 3: Complete Inspection Checklist
        print("\n🔄 Starting Inspection Checklist workflow...")
        checklist_page = InspectionChecklistPage(contractor_driver)
        checklist_page.complete_inspection_checklist()
        
        print("\n✅ Complete RFI workflow finished (RFI + Inspection Checklist).")
