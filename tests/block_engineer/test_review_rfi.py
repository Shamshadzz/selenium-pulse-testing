import pytest
from pages.block_engineer.review_rfi_page import ReviewRfiPage


@pytest.mark.block_engineer
class TestReviewRfi:
    """Block Engineer - RFI Review Tests"""

    def test_review_rfi_workflow(self, block_engineer_driver, base_url):
        """Test: Block Engineer reviews and approves RFI submission
        
        Workflow:
        1. Navigate to RFI review page
        2. Open pending RFI
        3. Add review comments
        4. Approve RFI
        5. Submit review
        """
        print("\n🔷 BLOCK ENGINEER: Review RFI Workflow")
        print("="*60)
        
        review_page = ReviewRfiPage(block_engineer_driver)
        
        # Navigate to review page
        review_page.navigate()
        
        # Complete review workflow
        review_page.review_rfi(
            comments="Reviewed all documentation and inspection checklist. Everything meets the requirements.",
            approve=True
        )
        
        # Verify success
        assert review_page.is_success_displayed(), "Review submission failed - no success message"
        print("✅ RFI Reviewed and Approved Successfully")
        print("="*60)

    def test_review_rfi_request_changes(self, block_engineer_driver, base_url):
        """Test: Block Engineer requests changes to RFI
        
        Workflow:
        1. Navigate to RFI review page
        2. Open pending RFI
        3. Add review comments with issues
        4. Request changes
        5. Submit review
        """
        print("\n🔷 BLOCK ENGINEER: Request Changes to RFI")
        print("="*60)
        
        review_page = ReviewRfiPage(block_engineer_driver)
        
        # Navigate to review page
        review_page.navigate()
        
        # Complete review workflow with changes requested
        review_page.review_rfi(
            comments="Issues found: Missing documentation in sections 3 and 5. Please resubmit after corrections.",
            approve=False
        )
        
        # Verify success
        assert review_page.is_success_displayed(), "Review submission failed - no success message"
        print("✅ Changes Requested Successfully")
        print("="*60)
