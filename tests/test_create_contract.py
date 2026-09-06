from datetime import datetime

import allure
import pytest


@allure.feature("Contracts")
@allure.story("Create contract")
@pytest.mark.ui
@pytest.mark.functional
def test_create_contract_successfully(contract_page):
    """Create a contract for Anh Tester 0109 and verify the saved details."""
    customer_name = "Anh Tester 0109"
    contract_type = "Thử việc"
    subject = f"Automation Contract {datetime.now():%Y%m%d%H%M%S}"

    with allure.step("Open the contract creation form"):
        contract_page.open_creation_form()

    with allure.step(f"Select customer: {customer_name}"):
        contract_page.select_customer(customer_name)

    with allure.step(f"Select contract type: {contract_type}"):
        contract_page.select_contract_type(contract_type)

    with allure.step(f"Fill contract subject: {subject}"):
        contract_page.fill_required_details(subject)

    with allure.step("Save the contract"):
        contract_page.save_contract()

    with allure.step("Verify the contract was created successfully"):
        contract_page.verify_contract_created(
            customer_name=customer_name,
            subject=subject,
            contract_type=contract_type,
        )