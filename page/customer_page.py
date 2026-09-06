from typing import Dict

from playwright.sync_api import Page

from page.base_page import BasePage


class CustomerPage(BasePage):
    """Page Object Model for creating and verifying a customer."""

    # ==================== Customer Page URLs and Locators ====================

    CUSTOMERS_URL = "/clients"
    CREATE_CUSTOMER_URL = "/clients/client"
    NEW_CUSTOMER_BUTTON = "//a[contains(.,'New Customer')]"  # TODO: Add locator strategy and value
    CUSTOMER_DETAILS_TAB = "//a[@aria-controls='contact_info']"  # TODO: Add locator strategy and value
    BILLING_SHIPPING_TAB = "//a[@aria-controls='billing_and_shipping']"  # TODO: Add locator strategy and value
    COMPANY_INPUT = "#company"  # TODO: Add locator strategy and value
    VAT_INPUT = "#vat"  # TODO: Add locator strategy and value
    PHONE_INPUT = "#phonenumber"  # TODO: Add locator strategy and value
    WEBSITE_INPUT = "#website"  # TODO: Add locator strategy and value
    ADDRESS_INPUT = "#address"  # TODO: Add locator strategy and value
    CITY_INPUT = "#city"  # TODO: Add locator strategy and value
    STATE_INPUT = "#state"  # TODO: Add locator strategy and value
    ZIP_INPUT = "#zip"  # TODO: Add locator strategy and value
    BILLING_STREET_INPUT = "#billing_street"  # TODO: Add locator strategy and value
    BILLING_CITY_INPUT = "#billing_city"  # TODO: Add locator strategy and value
    BILLING_STATE_INPUT = "#billing_state"  # TODO: Add locator strategy and value
    BILLING_ZIP_INPUT = "#billing_zip"  # TODO: Add locator strategy and value
    SHIPPING_STREET_INPUT = "#shipping_street"  # TODO: Add locator strategy and value
    SHIPPING_CITY_INPUT = "#shipping_city"  # TODO: Add locator strategy and value
    SHIPPING_STATE_INPUT = "#shipping_state"  # TODO: Add locator strategy and value
    SHIPPING_ZIP_INPUT = "#shipping_zip"  # TODO: Add locator strategy and value
    SAME_AS_CUSTOMER_INFO_BUTTON = "//a[contains(.,'Same as Customer Info')]"  # TODO: Add locator strategy and value
    COPY_BILLING_ADDRESS_BUTTON = "//a[contains(.,'Copy Billing Address')]"  # TODO: Add locator strategy and value
    SAVE_BUTTON = "//button[@class='btn btn-primary only-save customer-form-submiter']"  # TODO: Add locator strategy and value
    SUCCESS_TOAST = "#alert_float_1"  # TODO: Add locator strategy and value
    CUSTOMER_HEADER = "//div[@class='col-md-3']//h4"  # TODO: Add locator strategy and value
    COMPANY_VALUE = "#company"  # TODO: Add locator strategy and value

    # ==================== Initialization ====================

    def __init__(self, page: Page):
        super().__init__(page)

    # ==================== Create Customer ====================

    def open_customer_creation_form(self) -> None:
        """Open the customer creation form from the customers list."""
        self.navigate(self.CUSTOMERS_URL)
        self.click(self.NEW_CUSTOMER_BUTTON, "New Customer button")

    def verify_creation_form_is_displayed(self) -> None:
        """Verify the creation form opens on the default Customer Details tab."""
        assert self.page.url.endswith(self.CREATE_CUSTOMER_URL), (
            f"Unexpected customer creation URL: {self.page.url}"
        )
        self.expect_visible(self.CUSTOMER_DETAILS_TAB, "Customer Details tab")

    def fill_customer_details(self, customer_data: Dict[str, str]) -> None:
        """Fill the customer details supplied by the test."""
        field_locators = {
            "company": (self.COMPANY_INPUT, "Company"),
            "vat": (self.VAT_INPUT, "VAT Number"),
            "phone": (self.PHONE_INPUT, "Phone"),
            "website": (self.WEBSITE_INPUT, "Website"),
            "address": (self.ADDRESS_INPUT, "Address"),
            "city": (self.CITY_INPUT, "City"),
            "state": (self.STATE_INPUT, "State"),
            "zip_code": (self.ZIP_INPUT, "Zip Code"),
        }
        for field_name, (locator, label) in field_locators.items():
            value = customer_data.get(field_name)
            if value:
                self.fill(locator, value, label)

    # ==================== Billing and Shipping ====================

    def fill_billing_and_shipping(self, customer_data: Dict[str, str]) -> None:
        """Fill optional billing and shipping address fields."""
        self.click(self.BILLING_SHIPPING_TAB, "Billing & Shipping tab")
        field_locators = {
            "billing_street": (self.BILLING_STREET_INPUT, "Billing Street"),
            "billing_city": (self.BILLING_CITY_INPUT, "Billing City"),
            "billing_state": (self.BILLING_STATE_INPUT, "Billing State"),
            "billing_zip": (self.BILLING_ZIP_INPUT, "Billing Zip Code"),
            "shipping_street": (self.SHIPPING_STREET_INPUT, "Shipping Street"),
            "shipping_city": (self.SHIPPING_CITY_INPUT, "Shipping City"),
            "shipping_state": (self.SHIPPING_STATE_INPUT, "Shipping State"),
            "shipping_zip": (self.SHIPPING_ZIP_INPUT, "Shipping Zip Code"),
        }
        for field_name, (locator, label) in field_locators.items():
            value = customer_data.get(field_name)
            if value:
                self.fill(locator, value, label)

    # ==================== Save and Verify Customer ====================

    def save_customer(self) -> None:
        """Save the customer."""
        self.click(self.SAVE_BUTTON, "Save button")

    def verify_customer_created(self, company_name: str) -> None:
        """Verify the success toast, detail URL, and saved company name."""
        self.expect_visible(self.SUCCESS_TOAST, "customer created success toast")
        assert self.page.url.rstrip("/").split("/")[-2] == "client", (
            f"Expected customer detail URL, got: {self.page.url}"
        )
        self.expect_visible(self.CUSTOMER_HEADER, "customer detail header")
        self.expect_visible(self.COMPANY_VALUE, "saved company value")
        assert self.get_input_value(self.COMPANY_VALUE, "saved company value") == company_name