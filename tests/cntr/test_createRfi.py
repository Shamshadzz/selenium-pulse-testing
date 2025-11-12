import pytest
from pages.cntr.createRfi_page import CreateRfiPage


@pytest.mark.rfi
@pytest.mark.smoke
class TestCreateRfi:
    def test_create_rfi_complete(self, contractor_driver, base_url):
        """Test: Fill all RFI fields and submit."""
        page = CreateRfiPage(contractor_driver)
        page.navigate()
        page.create_rfi()

        assert page.is_element_visible(CreateRfiPage.SUCCESS_TOAST), \
            "RFI not created or success message missing."

        print("\n✅ RFI form filled and submitted successfully.")
