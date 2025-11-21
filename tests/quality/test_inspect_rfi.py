import pytest
from pages.quality.inspect_rfi_page import InspectRfiPage


@pytest.mark.quality
class TestInspectRfi:
    """Quality Inspector - RFI Inspection Tests"""

    def test_inspect_rfi_pass_workflow(self, quality_inspector_driver, base_url):
        """Test: Quality Inspector performs inspection and marks as PASS
        
        Workflow:
        1. Navigate to inspection queue
        2. Open pending RFI
        3. Complete quality checklist
        4. Add inspection findings
        5. Mark as PASS
        6. Submit inspection
        """
        print("\n🔷 QUALITY INSPECTOR: Inspect RFI - PASS")
        print("="*60)
        
        inspect_page = InspectRfiPage(quality_inspector_driver)
        
        # Navigate to inspection page
        inspect_page.navigate()
        
        # Complete inspection workflow
        inspect_page.perform_inspection(
            findings="All quality standards met. Materials verified. Workmanship excellent.",
            passed=True
        )
        
        # Verify success
        assert inspect_page.is_inspection_complete(), "Inspection submission failed - no success message"
        print("✅ RFI Inspection Completed - PASSED")
        print("="*60)

    def test_inspect_rfi_fail_workflow(self, quality_inspector_driver, base_url):
        """Test: Quality Inspector performs inspection and marks as FAIL
        
        Workflow:
        1. Navigate to inspection queue
        2. Open pending RFI
        3. Complete quality checklist
        4. Add inspection findings with issues
        5. Mark as FAIL
        6. Submit inspection
        """
        print("\n🔷 QUALITY INSPECTOR: Inspect RFI - FAIL")
        print("="*60)
        
        inspect_page = InspectRfiPage(quality_inspector_driver)
        
        # Navigate to inspection page
        inspect_page.navigate()
        
        # Complete inspection workflow with failure
        inspect_page.perform_inspection(
            findings="Quality issues found: Material does not meet specifications. Rework required.",
            passed=False
        )
        
        # Verify success
        assert inspect_page.is_inspection_complete(), "Inspection submission failed - no success message"
        print("✅ RFI Inspection Completed - FAILED (Rework Required)")
        print("="*60)

    def test_inspect_rfi_with_detailed_findings(self, quality_inspector_driver, base_url):
        """Test: Quality Inspector performs detailed inspection
        
        Workflow:
        1. Navigate to inspection queue
        2. Open pending RFI
        3. Complete quality checklist
        4. Add detailed inspection findings
        5. Mark as PASS
        6. Submit inspection
        """
        print("\n🔷 QUALITY INSPECTOR: Detailed Inspection")
        print("="*60)
        
        inspect_page = InspectRfiPage(quality_inspector_driver)
        
        # Navigate to inspection page
        inspect_page.navigate()
        
        # Detailed inspection
        detailed_findings = """
        Inspection Date: 2025-11-21
        Inspector: Quality Team
        
        Findings:
        - Material quality: Excellent
        - Installation accuracy: Within tolerance
        - Safety compliance: 100%
        - Documentation: Complete
        
        Recommendation: Approve
        """
        
        inspect_page.perform_inspection(
            findings=detailed_findings.strip(),
            passed=True
        )
        
        # Verify success
        assert inspect_page.is_inspection_complete(), "Inspection submission failed - no success message"
        print("✅ Detailed Inspection Completed Successfully")
        print("="*60)
