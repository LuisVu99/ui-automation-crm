from datetime import datetime

import allure
import pytest


@allure.feature("Contracts")
@allure.story("Edit contract")
@pytest.mark.ui
@pytest.mark.functional
def test_edit_contract_successfully(contract_page):
    """Create a minimal contract, edit its required subject, and verify the update."""
    customer_name = "Anh Tester 0109"
    updated_customer_name = "HKD Anh Tester"
    original_subject = f"Edit Contract {datetime.now():%Y%m%d%H%M%S}"
    updated_subject = f"Edited Contract {datetime.now():%Y%m%d%H%M%S}"
    updated_start_date = "15-09-2026"

    with allure.step("Create a minimal contract with the required fields"):
        contract_page.open_creation_form()
        contract_page.select_customer(customer_name)
        contract_page.fill_required_details(original_subject)
        contract_page.save_contract()
        contract_page.expect_visible(
            contract_page.SUCCESS_TOAST,
            "Contract creation success toast",
        )

    with allure.step("Navigate back to the contracts list"):
        contract_page.return_to_contracts_list()

    with allure.step(f"Search for the created contract: {original_subject}"):
        contract_page.search_contract(original_subject)

    with allure.step("Hover over the subject and reveal the Edit action"):
        contract_page.show_edit_action(original_subject)

    with allure.step("Open the contract edit page"):
        contract_page.open_edit_form()

    with allure.step("Clear the old customer, select HKD Anh Tester, and update required fields"):
        contract_page.update_required_details(
            updated_customer_name,
            updated_subject,
            updated_start_date,
        )
        contract_page.save_contract()

    with allure.step("Verify the contract was modified successfully"):
        contract_page.verify_contract_updated(
            updated_customer_name,
            updated_subject,
            updated_start_date,
        )