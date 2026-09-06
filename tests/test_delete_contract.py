from datetime import datetime

import allure
import pytest


@allure.feature("Contracts")
@allure.story("Delete contract")
@pytest.mark.ui
@pytest.mark.functional
def test_delete_contract_successfully(contract_page):
    """Create a minimal contract, then delete it from the contracts list."""
    customer_name = "Anh Tester 0109"
    subject = f"Delete Contract {datetime.now():%Y%m%d%H%M%S}"

    with allure.step("Create a minimal contract for delete testing"):
        contract_page.open_creation_form()
        contract_page.select_customer(customer_name)
        contract_page.fill_required_details(subject)
        contract_page.save_contract()
        contract_page.expect_visible(
            contract_page.SUCCESS_TOAST,
            "Contract creation success toast",
        )

    with allure.step("Return to the contracts list"):
        contract_page.return_to_contracts_list()

    with allure.step(f"Search for the created contract: {subject}"):
        contract_page.search_contract(subject)

    with allure.step("Hover over the contract Subject and show Delete action"):
        contract_page.show_delete_action(subject)

    with allure.step("Click Delete and accept the native OK confirmation popup"):
        contract_page.delete_contract()

    with allure.step("Verify the contract was deleted successfully"):
        contract_page.verify_contract_deleted()