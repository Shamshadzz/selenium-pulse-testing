import pytest
from pages.block_engineer.approve_rfi_page import ApproveRfiPage


@pytest.mark.block_engineer
class TestApproveRfi:
    """Block Engineer - RFI Final Approval Tests"""

    def test_approve_rfi_workflow(self, block_engineer_driver, base_url):
        """Test: Block Engineer gives final approval to RFI
        
        Workflow:
        1. Navigate to approved RFI list
        2. Open RFI for final approval
        3. Add approval notes
        4. Give final approval
        5. Confirm
        """
        print("\n🔷 BLOCK ENGINEER: Final Approval Workflow")
        print("="*60)
        
        approve_page = ApproveRfiPage(block_engineer_driver)
        
        # Navigate to approval page
        approve_page.navigate()
        
        # Complete approval workflow
        approve_page.approve_rfi(
            notes="All requirements met. Quality standards verified. Final approval granted."
        )
        
        # Verify success
        assert approve_page.is_success_displayed(), "Approval failed - no success message"
        print("✅ RFI Final Approval Granted Successfully")
        print("="*60)

    def test_approve_rfi_with_conditions(self, block_engineer_driver, base_url):
        """Test: Block Engineer approves RFI with conditions
        
        Workflow:
        1. Navigate to approved RFI list
        2. Open RFI for final approval
        3. Add conditional approval notes
        4. Give approval
        """
        print("\n🔷 BLOCK ENGINEER: Conditional Approval")
        print("="*60)
        
        approve_page = ApproveRfiPage(block_engineer_driver)
        
        # Navigate to approval page
        approve_page.navigate()
        
        # Complete approval with conditions
        approve_page.approve_rfi(
            notes="Approved with conditions: Monitor progress for next 2 weeks and submit progress report."
        )
        
        # Verify success
        assert approve_page.is_success_displayed(), "Approval failed - no success message"
        print("✅ Conditional Approval Granted Successfully")
        print("="*60)
