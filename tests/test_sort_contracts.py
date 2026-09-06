import allure
import pytest


SORT_COLUMNS = ["Subject", "Customer", "Contract Value", "Start Date"]


@allure.feature("Contracts")
@allure.story("Sort contracts list")
@pytest.mark.skip()
@pytest.mark.ui
@pytest.mark.functional
@pytest.mark.parametrize("column_name", SORT_COLUMNS)
def test_sort_contracts_by_column_ascending(contract_page, column_name):
    """The first click sorts the currently displayed contracts ascending."""
    with allure.step("Open the Contracts list and wait for the table"):
        contract_page.open_contracts_list()

    with allure.step(f"Sort the current rows by {column_name} ascending"):
        initial_values = contract_page.get_contract_column_values(column_name)
        contract_page.sort_contracts_by(column_name)
        actual_values = contract_page.get_contract_column_values(column_name)

    assert len(initial_values) >= 2, (
        f"At least two displayed contracts are required to verify {column_name} sort"
    )
    expected_values = sorted(
        initial_values,
        key=lambda value: contract_page.contract_sort_key(column_name, value),
    )
    assert actual_values == expected_values, (
        f"{column_name} was not sorted ascending on the first click: "
        f"actual={actual_values!r}, expected={expected_values!r}"
    )


@allure.feature("Contracts")
@allure.story("Sort contracts list")
@pytest.mark.skip()
@pytest.mark.ui
@pytest.mark.functional
@pytest.mark.parametrize("column_name", SORT_COLUMNS)
def test_sort_contracts_by_column_descending_on_second_click(contract_page, column_name):
    """The second click reverses the order of the currently displayed rows."""
    with allure.step("Open the Contracts list and wait for the table"):
        contract_page.open_contracts_list()

    with allure.step(f"Sort the current rows by {column_name} twice"):
        initial_values = contract_page.get_contract_column_values(column_name)
        contract_page.sort_contracts_by(column_name)
        contract_page.click_contract_sort_header(column_name, "descending")
        actual_values = contract_page.get_contract_column_values(column_name)

    assert len(initial_values) >= 2, (
        f"At least two displayed contracts are required to verify {column_name} sort"
    )
    non_empty_values = [value for value in initial_values if value]
    empty_values = [value for value in initial_values if not value]
    expected_values = empty_values + sorted(
        non_empty_values,
        key=lambda value: contract_page.contract_sort_key(column_name, value),
        reverse=True,
    )
    assert actual_values == expected_values, (
        f"{column_name} was not sorted descending on the second click: "
        f"actual={actual_values!r}, expected={expected_values!r}"
    )