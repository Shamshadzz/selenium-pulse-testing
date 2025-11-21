import pytest
from pages.quality.final_approval_page import FinalApprovalPage


@pytest.mark.quality
class TestFinalApproval:
    """Quality Inspector - Final Approval Tests"""

    def test_final_approval_workflow(self, quality_inspector_driver, base_url):
        """Test: Quality Inspector gives final approval and closes RFI
        
        Workflow:
        1. Navigate to inspected RFIs
        2. Open inspected RFI
        3. Add final remarks
        4. Give final approval
        5. Close RFI
        """
        print("\n🔷 QUALITY INSPECTOR: Final Approval & Close RFI")
        print("="*60)
        
        final_approval_page = FinalApprovalPage(quality_inspector_driver)
        
        # Navigate to inspected RFIs
        final_approval_page.navigate()
        
        # Complete final approval workflow
        final_approval_page.give_final_approval(
            remarks="Quality inspection passed. All requirements met. RFI closed successfully."
        )
        
        # Verify success
        assert final_approval_page.is_success_displayed(), "Final approval failed - no success message"
        print("✅ Final Approval Granted & RFI Closed")
        print("="*60)

    def test_final_approval_with_recommendations(self, quality_inspector_driver, base_url):
        """Test: Quality Inspector gives final approval with recommendations
        
        Workflow:
        1. Navigate to inspected RFIs
        2. Open inspected RFI
        3. Add final remarks with recommendations
        4. Give final approval
        """
        print("\n🔷 QUALITY INSPECTOR: Final Approval with Recommendations")
        print("="*60)
        
        final_approval_page = FinalApprovalPage(quality_inspector_driver)
        
        # Navigate to inspected RFIs
        final_approval_page.navigate()
        
        # Final approval with recommendations
        final_approval_page.give_final_approval(
            remarks="Approved with recommendations: Consider implementing preventive measures for future similar work."
        )
        
        # Verify success
        assert final_approval_page.is_success_displayed(), "Final approval failed - no success message"
        print("✅ Final Approval with Recommendations Granted")
        print("="*60)

    def test_final_approval_detailed_report(self, quality_inspector_driver, base_url):
        """Test: Quality Inspector gives final approval with detailed report
        
        Workflow:
        1. Navigate to inspected RFIs
        2. Open inspected RFI
        3. Add detailed final report
        4. Give final approval
        """
        print("\n🔷 QUALITY INSPECTOR: Final Approval with Detailed Report")
        print("="*60)
        
        final_approval_page = FinalApprovalPage(quality_inspector_driver)
        
        # Navigate to inspected RFIs
        final_approval_page.navigate()
        
        # Detailed final report
        detailed_report = """
        Final Quality Report
        ====================
        Date: 2025-11-21
        Inspector: QA Team Lead
        
        Summary:
        - All inspection checkpoints verified
        - Quality standards exceeded expectations
        - Documentation complete and accurate
        - Safety protocols fully complied
        
        Final Decision: APPROVED
        RFI Status: CLOSED
        """
        
        final_approval_page.give_final_approval(
            remarks=detailed_report.strip()
        )
        
        # Verify success
        assert final_approval_page.is_success_displayed(), "Final approval failed - no success message"
        print("✅ Final Approval with Detailed Report Completed")
        print("="*60)
