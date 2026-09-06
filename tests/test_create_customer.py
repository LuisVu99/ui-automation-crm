from datetime import datetime

import allure
import pytest


@allure.feature("Customers")
@allure.story("Create customer")
@pytest.mark.ui
@pytest.mark.functional
def test_create_customer_successfully(customer_page):
    """Create a customer and verify it is shown on the detail page."""
    company_name = f"Automation Customer {datetime.now():%Y%m%d%H%M%S}"
    customer_data = {
        "company": company_name,
        "vat": "VAT-001",
        "phone": "0901234567",
        "website": "https://example.com",
        "address": "123 Automation Street",
        "city": "Ho Chi Minh",
        "state": "Ho Chi Minh",
        "zip_code": "700000",
        "billing_street": "123 Automation Street",
        "billing_city": "Ho Chi Minh",
        "billing_state": "Ho Chi Minh",
        "billing_zip": "700000",
        "shipping_street": "123 Automation Street",
        "shipping_city": "Ho Chi Minh",
        "shipping_state": "Ho Chi Minh",
        "shipping_zip": "700000",
    }

    with allure.step("Open the customer creation form"):
        customer_page.open_customer_creation_form()
        customer_page.verify_creation_form_is_displayed()

    with allure.step(f"Fill customer details for {company_name}"):
        customer_page.fill_customer_details(customer_data)

    with allure.step("Fill billing and shipping addresses"):
        customer_page.fill_billing_and_shipping(customer_data)

    with allure.step("Save the customer"):
        customer_page.save_customer()

    with allure.step("Verify the customer was created successfully"):
        customer_page.verify_customer_created(company_name)