from datetime import datetime
import re

from playwright.sync_api import Page

from page.base_page import BasePage


class ContractPage(BasePage):
    """Page Object Model for creating and verifying a contract."""

    # ==================== Contract Page URLs and Locators ====================

    CONTRACTS_URL = "/contracts"
    NEW_CONTRACT_BUTTON = "//a[contains(.,'New Contract')]"  # TODO: Add locator strategy and value
    CONTRACT_INFORMATION_HEADING = "//h4[contains(.,'Contract Information')]"  # TODO: Add locator strategy and value
    CUSTOMER_FIELD = "//button[@data-id='clientid']"  # TODO: Add locator strategy and value
    CUSTOMER_CLEAR_BUTTON = "//span[@data-id='clientid']"  # TODO: Add locator for the x button that clears the selected customer
    CUSTOMER_SEARCH_INPUT = "//input[@aria-controls='bs-select-2']"  # TODO: Add locator strategy and value
    CUSTOMER_OPTION = "//a[normalize-space()='{customer_name}']"  # TODO: Add locator strategy and value
    SUBJECT_INPUT = "#subject"  # TODO: Add locator strategy and value
    CONTRACT_TYPE_FIELD = "//button[@aria-owns='bs-select-1']"  # TODO: Add locator strategy and value
    CONTRACT_TYPE_SEARCH_INPUT = "//input[@aria-controls='bs-select-1']"  # TODO: Add locator strategy and value
    CONTRACT_TYPE_OPTION = "//a[.='Thử việc']"  # TODO: Add locator strategy and value
    START_DATE_INPUT = "#datestart"  # TODO: Add locator strategy and value
    SAVE_BUTTON = "(//button[@type='submit'])[1]"  # TODO: Add locator strategy and value
    SUCCESS_TOAST = "#alert_float_1"  # TODO: Add locator strategy and value
    CONTRACT_DETAIL = "//h4[contains(.,'Contract Information')]"  # TODO: Add locator strategy and value
    CUSTOMER_VALUE = "//button[@data-id='clientid']"  # TODO: Add locator strategy and value
    SUBJECT_VALUE = "#subject"  # TODO: Add locator strategy and value
    CONTRACT_TYPE_VALUE = "//button[@data-id='contract_type']"  # TODO: Add locator strategy and value
    CONTRACT_SEARCH_INPUT = "//input[@aria-controls='contracts']"  # TODO: Add locator strategy and value
    CONTRACT_ROW = "//table[@id='contracts']//tbody//tr"  # TODO: Add locator strategy and value
    CONTRACT_HEADERS = "#contracts thead th"
    CONTRACT_TABLE_ROWS = "#contracts tbody tr"
    CONTRACT_SUBJECT_LINK = "//table[@id='contracts']//tbody//tr/td[2]"  # TODO: Add locator strategy and value
    EDIT_BUTTON = "//a[.='Edit ']"  # TODO: Add locator for the Edit action revealed on contract hover
    DELETE_BUTTON = "//a[@class='text-danger _delete']"  # TODO: Add locator strategy and value
    DELETE_SUCCESS_TOAST = "#alert_float_1"  # TODO: Add locator strategy and value

    # ==================== Initialization ====================

    def __init__(self, page: Page):
        super().__init__(page)

    # ==================== Create Contract ====================

    def open_creation_form(self) -> None:
        """Open the new contract form and wait for it to load."""
        self.navigate(self.CONTRACTS_URL)
        self.wait_for_load_page()
        self.click(self.NEW_CONTRACT_BUTTON, "New Contract button")
        self.wait_for_load_page()
        self.expect_visible(
            self.CONTRACT_INFORMATION_HEADING,
            "Contract Information heading",
        )

    def select_customer(self, customer_name: str) -> None:
        """Search for and select a customer from the customer combobox."""
        self.click(self.CUSTOMER_FIELD, "Customer field")
        self.type_text(self.CUSTOMER_SEARCH_INPUT, customer_name, "Customer search")
        customer_option = self.CUSTOMER_OPTION.format(customer_name=customer_name)
        self.wait_for_selector(customer_option, "Customer search result")
        self.click(customer_option, f"Customer option: {customer_name}")

    def replace_customer(self, customer_name: str) -> None:
        """Clear the current customer, then search for and select a replacement."""
        self.click(self.CUSTOMER_CLEAR_BUTTON, "Clear selected customer")
        self.select_customer(customer_name)

    def select_contract_type(self, contract_type: str) -> None:
        """Search for and select a contract type."""
        self.click(self.CONTRACT_TYPE_FIELD, "Contract type field")
        self.type_text(
            self.CONTRACT_TYPE_SEARCH_INPUT,
            contract_type,
            "Contract type search",
        )
        self.wait_for_selector(
            self.CONTRACT_TYPE_OPTION,
            "Contract type search result",
        )
        self.click(
            self.CONTRACT_TYPE_OPTION,
            f"Contract type option: {contract_type}",
        )

    def fill_required_details(self, subject: str) -> None:
        """Fill the required subject while preserving the default start date."""
        self.fill(self.SUBJECT_INPUT, subject, "Subject")
        self.expect_visible(self.START_DATE_INPUT, "Start Date")

    def save_contract(self) -> None:
        """Save the contract and wait for the detail page to load."""
        self.click(self.SAVE_BUTTON, "Save button")
        self.wait_for_load_page()

    # ==================== View Contracts ====================

    def return_to_contracts_list(self) -> None:
        """Navigate back to the contracts list and wait for it to load."""
        self.navigate(self.CONTRACTS_URL)
        self.wait_for_load_page()

    def open_contracts_list(self) -> None:
        """Open the contracts list and wait for its table to be available."""
        self.navigate(self.CONTRACTS_URL)
        self.wait_for_load_page()
        self.wait_for_selector(self.CONTRACT_TABLE_ROWS, "Contracts table rows")
        processing_indicator = self.page.locator("#contracts_processing")
        if processing_indicator.count():
            processing_indicator.wait_for(state="hidden")

    def sort_contracts_by(self, column_name: str) -> None:
        """Click a contract table header once and wait for ascending sort."""
        self.click_contract_sort_header(column_name, "ascending")

    def click_contract_sort_header(self, column_name: str, direction: str) -> None:
        """Click a contract header and wait for the requested sort direction."""
        headers = self.page.locator(self.CONTRACT_HEADERS)
        header_count = headers.count()
        column_index = next(
            (
                index
                for index in range(header_count)
                if headers.nth(index).inner_text().strip() == column_name
            ),
            None,
        )
        assert column_index is not None, (
            f"Contract sort header was not found: {column_name!r}"
        )

        header = headers.nth(column_index)
        header.click()
        class_name = "sorting_asc" if direction == "ascending" else "sorting_desc"
        self.page.wait_for_function(
            """
            ({ index, className, ariaSort }) => {
                const header = document.querySelectorAll('#contracts thead th')[index];
                return header && (
                    header.classList.contains(className) ||
                    header.getAttribute('aria-sort') === ariaSort
                );
            }
            """,
            arg={
                "index": column_index,
                "className": class_name,
                "ariaSort": direction,
            },
        )

    # ==================== Search and Read Contract Data ====================

    def get_contract_column_values(self, column_name: str) -> list[str]:
        """Return values for a column from the rows currently displayed."""
        headers = self.page.locator(self.CONTRACT_HEADERS)
        column_index = next(
            (
                index
                for index in range(headers.count())
                if headers.nth(index).inner_text().strip() == column_name
            ),
            None,
        )
        assert column_index is not None, (
            f"Contract column was not found: {column_name!r}"
        )

        rows = self.page.locator(self.CONTRACT_TABLE_ROWS)
        values = []
        for row_index in range(rows.count()):
            row = rows.nth(row_index)
            cells = row.locator("td")
            cell = cells.nth(column_index)
            if column_name in {"Subject", "Customer"} and cell.locator("a").count():
                values.append(cell.locator("a").first.inner_text().strip())
            else:
                values.append(cell.inner_text().strip())
        return values

    @staticmethod
    def contract_sort_key(column_name: str, value: str) -> tuple[int, object]:
        """Build the expected ascending key for a displayed contract value."""
        if column_name in {"Subject", "Customer"}:
            return (0 if not value else 1, value.casefold())
        if column_name == "Contract Value":
            numeric_value = re.sub(r"[^0-9.-]", "", value) or "0"
            return (1, float(numeric_value))
        if column_name == "Start Date":
            if not value:
                return (0, datetime.min)
            return (1, datetime.strptime(value, "%d-%m-%Y"))
        raise ValueError(f"Unsupported contract sort column: {column_name}")

    def search_contract(self, subject: str) -> None:
        """Search the contracts list by Subject."""
        self.type_text(self.CONTRACT_SEARCH_INPUT, subject, "Contract search")
        self.wait_for_selector(self.CONTRACT_ROW, "Contract search result")

    # ==================== Edit Contract ====================

    def show_delete_action(self, subject: str) -> None:
        """Hover the matching contract Subject to reveal row actions."""
        self.hover(self.CONTRACT_SUBJECT_LINK, f"Contract Subject: {subject}")
        self.expect_visible(self.DELETE_BUTTON, "Delete contract button")

    def show_edit_action(self, subject: str) -> None:
        """Hover the matching contract Subject to reveal the Edit action."""
        self.hover(self.CONTRACT_SUBJECT_LINK, f"Contract Subject: {subject}")
        self.expect_visible(self.EDIT_BUTTON, "Edit contract button")

    def open_edit_form(self) -> None:
        """Open the contract edit form and wait for it to load."""
        self.click(self.EDIT_BUTTON, "Edit contract button")
        self.wait_for_load_page()
        self.expect_visible(self.CONTRACT_INFORMATION_HEADING, "Contract Information heading")

    def update_required_details(
        self,
        customer_name: str,
        subject: str,
        start_date: str,
    ) -> None:
        """Update the editable customer, subject, and start date."""
        self.replace_customer(customer_name)
        self.fill(self.SUBJECT_INPUT, subject, "Updated subject")
        self.fill(self.START_DATE_INPUT, start_date, "Updated start date")
        self.expect_visible(self.START_DATE_INPUT, "Start Date")

    def verify_contract_updated(
        self,
        customer_name: str,
        subject: str,
        start_date: str,
    ) -> None:
        """Verify the update toast and updated required values."""
        self.expect_visible(self.SUCCESS_TOAST, "Contract update success toast")
        actual_customer = self.get_text(self.CUSTOMER_VALUE, "Updated customer")
        assert actual_customer == customer_name, (
            "Updated customer assertion failed: "
            f"expected={customer_name!r}, actual={actual_customer!r}"
        )
        actual_subject = self.get_attribute(self.SUBJECT_VALUE, "value", "Updated subject")
        assert actual_subject == subject, (
            "Updated subject assertion failed: "
            f"expected={subject!r}, actual={actual_subject!r}"
        )
        actual_start_date = self.get_attribute(
            self.START_DATE_INPUT,
            "value",
            "Updated start date",
        )
        assert actual_start_date == start_date, (
            "Updated start date assertion failed: "
            f"expected={start_date!r}, actual={actual_start_date!r}"
        )

    # ==================== Delete Contract ====================

    def delete_contract(self) -> None:
        """Delete the visible contract and accept the native browser dialog."""
        def handle_dialog(dialog):
            assert dialog.type == "confirm", (
                "Delete dialog assertion failed: "
                f"expected='confirm', actual={dialog.type!r}"
            )
            assert dialog.message == "Are you sure you want to perform this action?", (
                "Delete dialog message assertion failed: "
                "expected='Are you sure you want to perform this action?', "
                f"actual={dialog.message!r}"
            )
            dialog.accept()

        # Đăng ký handler bắt sự kiện dialog trước khi click
        self.page.once("dialog", handle_dialog)
        self.click(self.DELETE_BUTTON, "Delete contract button")
        self.wait_for_load_page()

    def verify_contract_deleted(self) -> None:
        """Verify that the delete success notification is displayed."""
        self.expect_visible(self.DELETE_SUCCESS_TOAST, "Contract delete success toast")

    # ==================== Contract Creation Verification ====================

    def verify_contract_created(
        self,
        customer_name: str,
        subject: str,
        contract_type: str,
    ) -> None:
        """Verify the success notification and values on the detail page."""
        self.expect_visible(self.SUCCESS_TOAST, "Contract success toast")
        self.expect_visible(self.CONTRACT_DETAIL, "Contract detail")
        self.expect_visible(self.CUSTOMER_VALUE, "Saved customer")
        self.expect_visible(self.SUBJECT_VALUE, "Saved subject")
        self.expect_visible(self.CONTRACT_TYPE_VALUE, "Saved contract type")

        actual_customer = self.get_text(self.CUSTOMER_VALUE, "Saved customer")
        assert actual_customer == customer_name, (
            "Customer assertion failed: "
            f"expected={customer_name!r}, actual={actual_customer!r}"
        )

        actual_subject = self.get_attribute(self.SUBJECT_VALUE, "value", "Saved subject")
        assert actual_subject == subject, (
            "Subject assertion failed: "
            f"expected={subject!r}, actual={actual_subject!r}"
        )

        actual_contract_type = self.get_attribute(
            self.CONTRACT_TYPE_VALUE,
            "title",
            "Saved contract type",
        )
        assert actual_contract_type == contract_type, (
            "Contract type assertion failed: "
            f"expected={contract_type!r}, actual={actual_contract_type!r}"
        )