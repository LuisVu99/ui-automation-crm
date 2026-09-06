from page.base_page import BasePage
from playwright.sync_api import Locator, Page
from typing import List, Optional
import time


class DashboardPage(BasePage):
    """
    Dashboard Page Object Model.
    
    This page represents the main dashboard screen and handles all dashboard-specific
    interactions. Locators and actions are clearly separated for maintainability.
    """

    # ==================== Locator Selectors (Private Constants) ====================
    
    _LEFT_MENU_SELECTOR = "#menu"
    _SEARCH_INPUT_SELECTOR = "#search_input"
    _SEARCH_BUTTON_SELECTOR = "//div[@id='top_search_button']//button"
    _SEARCH_RESULTS_SELECTOR = "//div[@id='search_results']//li//a"
    _FIRST_SEARCH_RESULT_SELECTOR = "//a[.='Anh Tester 09072025A2']"
    _DASHBOARD_HIGHLIGHTED_SELECTOR = "//li[@class='menu-item-dashboard active']"
    
    # Widget selectors
    _WIDGET_TOP_STATS_SELECTOR = "#widget-top_stats"
    _WIDGET_FINANCE_OVERVIEW_SELECTOR = "#widget-finance_overview"
    _WIDGET_USER_DATA_SELECTOR = "#widget-user_data"
    _WIDGET_CALENDAR_SELECTOR = "#widget-calendar"
    _WIDGET_PAYMENT_CHART_SELECTOR = "#widget-payments_chart"
    _WIDGET_CONTRACT_EXPIRED_SELECTOR = "#widget-contracts_expiring"
    _WIDGET_TODO_ITEMS_SELECTOR = "#widget-todos"
    _WIDGET_LEAD_CHART_SELECTOR = "#widget-leads_chart"
    _WIDGET_PROJECT_CHART_SELECTOR = "#widget-projects_chart"
    _WIDGET_PROJECT_ACTIVITY_SELECTOR = "#widget-projects_activity"
    
    # Progress bar selectors
    _INVOICE_PROGRESS_FRACTION_SELECTOR = "(//div[contains(@class,'quick-stats-invoices')]/div[1]//span)[2]"
    _INVOICE_PROGRESS_PERCENT_SELECTOR = "//div[contains(@class,'quick-stats-invoices')]//div[@role='progressbar']"
    _LEAD_PROGRESS_FRACTION_SELECTOR = "(//div[contains(@class,'quick-stats-leads')]/div[1]//span)[2]"
    _LEAD_PROGRESS_PERCENT_SELECTOR = "//div[contains(@class,'quick-stats-leads')]//div[@role='progressbar']"
    _PROJECT_PROGRESS_FRACTION_SELECTOR = "(//div[contains(@class,'quick-stats-projects')]/div[1]//span)[2]"
    _PROJECT_PROGRESS_PERCENT_SELECTOR = "//div[contains(@class,'quick-stats-projects')]//div[@role='progressbar']"
    _TASK_PROGRESS_FRACTION_SELECTOR = "(//div[contains(@class,'quick-stats-tasks')]/div[1]//span)[2]"
    _TASK_PROGRESS_PERCENT_SELECTOR = "//div[contains(@class,'quick-stats-tasks')]//div[@role='progressbar']"
    
    # Icon header selectors
    _ICON_NEWSFEED_SELECTOR = "//li[@class='icon header-newsfeed']"
    _ICON_TODO_SELECTOR = "//li[@class='icon header-todo']"
    _ICON_USER_PROFILE_SELECTOR = "//li[@class='icon header-user-profile']"
    _ICON_TIMESHEETS_SELECTOR = "//li[@data-title='My Timesheets']"
    _ICON_NOTIFICATIONS_SELECTOR = "//li[@title='Notifications']"

    # ==================== Locators as Properties ====================
    
    @property
    def left_menu(self) -> Locator:
        """Left navigation menu."""
        return self.page.locator(self._LEFT_MENU_SELECTOR)

    @property
    def search_input(self) -> Locator:
        """Search input field."""
        return self.page.locator(self._SEARCH_INPUT_SELECTOR)

    @property
    def search_button(self) -> Locator:
        """Search submission button."""
        return self.page.locator(self._SEARCH_BUTTON_SELECTOR)

    @property
    def search_results(self) -> Locator:
        """Search results list items."""
        return self.page.locator(self._SEARCH_RESULTS_SELECTOR)

    @property
    def first_search_result(self) -> Locator:
        """First search result item."""
        return self.page.locator(self._FIRST_SEARCH_RESULT_SELECTOR)

    @property
    def dashboard_highlighted(self) -> Locator:
        """Dashboard menu item when active."""
        return self.page.locator(self._DASHBOARD_HIGHLIGHTED_SELECTOR)

    # ==================== Widget Locators ====================
    
    @property
    def widget_top_stats(self) -> Locator:
        """Top statistics widget."""
        return self.page.locator(self._WIDGET_TOP_STATS_SELECTOR)

    @property
    def widget_finance_overview(self) -> Locator:
        """Finance overview widget."""
        return self.page.locator(self._WIDGET_FINANCE_OVERVIEW_SELECTOR)

    @property
    def widget_user_data(self) -> Locator:
        """User data widget."""
        return self.page.locator(self._WIDGET_USER_DATA_SELECTOR)

    @property
    def widget_calendar(self) -> Locator:
        """Calendar widget."""
        return self.page.locator(self._WIDGET_CALENDAR_SELECTOR)

    @property
    def widget_payment_chart(self) -> Locator:
        """Payment chart widget."""
        return self.page.locator(self._WIDGET_PAYMENT_CHART_SELECTOR)

    @property
    def widget_contract_expired(self) -> Locator:
        """Contracts expiring widget."""
        return self.page.locator(self._WIDGET_CONTRACT_EXPIRED_SELECTOR)

    @property
    def widget_todo_items(self) -> Locator:
        """To-do items widget."""
        return self.page.locator(self._WIDGET_TODO_ITEMS_SELECTOR)

    @property
    def widget_lead_chart(self) -> Locator:
        """Lead chart widget."""
        return self.page.locator(self._WIDGET_LEAD_CHART_SELECTOR)

    @property
    def widget_project_chart(self) -> Locator:
        """Project chart widget."""
        return self.page.locator(self._WIDGET_PROJECT_CHART_SELECTOR)

    @property
    def widget_project_activity(self) -> Locator:
        """Project activity widget."""
        return self.page.locator(self._WIDGET_PROJECT_ACTIVITY_SELECTOR)

    @property
    def all_widgets(self) -> List[Locator]:
        """All dashboard widgets."""
        return [
            self.widget_top_stats,
            self.widget_finance_overview,
            self.widget_user_data,
            self.widget_calendar,
            self.widget_payment_chart,
            self.widget_contract_expired,
            self.widget_todo_items,
            self.widget_lead_chart,
            self.widget_project_chart,
            self.widget_project_activity,
        ]

    # ==================== Progress Bar Locators ====================
    
    @property
    def invoice_progress_fraction(self) -> Locator:
        """Invoice progress fraction display."""
        return self.page.locator(self._INVOICE_PROGRESS_FRACTION_SELECTOR)

    @property
    def invoice_progress_percent(self) -> Locator:
        """Invoice progress percentage bar."""
        return self.page.locator(self._INVOICE_PROGRESS_PERCENT_SELECTOR)

    @property
    def lead_progress_fraction(self) -> Locator:
        """Lead progress fraction display."""
        return self.page.locator(self._LEAD_PROGRESS_FRACTION_SELECTOR)

    @property
    def lead_progress_percent(self) -> Locator:
        """Lead progress percentage bar."""
        return self.page.locator(self._LEAD_PROGRESS_PERCENT_SELECTOR)

    @property
    def project_progress_fraction(self) -> Locator:
        """Project progress fraction display."""
        return self.page.locator(self._PROJECT_PROGRESS_FRACTION_SELECTOR)

    @property
    def project_progress_percent(self) -> Locator:
        """Project progress percentage bar."""
        return self.page.locator(self._PROJECT_PROGRESS_PERCENT_SELECTOR)

    @property
    def task_progress_fraction(self) -> Locator:
        """Task progress fraction display."""
        return self.page.locator(self._TASK_PROGRESS_FRACTION_SELECTOR)

    @property
    def task_progress_percent(self) -> Locator:
        """Task progress percentage bar."""
        return self.page.locator(self._TASK_PROGRESS_PERCENT_SELECTOR)

    # ==================== Icon Header Locators ====================
    
    @property
    def icon_newsfeed(self) -> Locator:
        """Newsfeed icon in header."""
        return self.page.locator(self._ICON_NEWSFEED_SELECTOR)

    @property
    def icon_todo(self) -> Locator:
        """To-do icon in header."""
        return self.page.locator(self._ICON_TODO_SELECTOR)

    @property
    def icon_user_profile(self) -> Locator:
        """User profile icon in header."""
        return self.page.locator(self._ICON_USER_PROFILE_SELECTOR)

    @property
    def icon_timesheets(self) -> Locator:
        """Timesheets icon in header."""
        return self.page.locator(self._ICON_TIMESHEETS_SELECTOR)

    @property
    def icon_notifications(self) -> Locator:
        """Notifications icon in header."""
        return self.page.locator(self._ICON_NOTIFICATIONS_SELECTOR)

    @property
    def all_header_icons(self) -> List[Locator]:
        """All header icon elements."""
        return [
            self.icon_newsfeed,
            self.icon_todo,
            self.icon_user_profile,
            self.icon_timesheets,
            self.icon_notifications,
        ]

    # ==================== Dashboard Verification ====================

    def verify_left_menu_is_visible(self) -> bool:
        """
        Verify that the left navigation menu is visible.
        
        Returns:
            True if menu is visible
        """
        return self.is_visible(
            self._LEFT_MENU_SELECTOR,
            name="left menu"
        )

    def verify_all_widgets_visible(self) -> None:
        """
        Verify that all dashboard widgets are visible.
        
        Raises:
            AssertionError if any widget is not visible
        """
        widget_selectors = [
            self._WIDGET_TOP_STATS_SELECTOR,
            self._WIDGET_FINANCE_OVERVIEW_SELECTOR,
            self._WIDGET_USER_DATA_SELECTOR,
            self._WIDGET_CALENDAR_SELECTOR,
            self._WIDGET_PAYMENT_CHART_SELECTOR,
            self._WIDGET_CONTRACT_EXPIRED_SELECTOR,
            self._WIDGET_TODO_ITEMS_SELECTOR,
            self._WIDGET_LEAD_CHART_SELECTOR,
            self._WIDGET_PROJECT_CHART_SELECTOR,
            self._WIDGET_PROJECT_ACTIVITY_SELECTOR,
        ]
        for i, selector in enumerate(widget_selectors):
            self.expect_visible(selector, name=f"widget {i}")

    def verify_dashboard_is_active(self) -> bool:
        """
        Verify that dashboard menu item is highlighted as active.
        
        Returns:
            True if dashboard is marked active
        """
        return self.is_visible(
            self._DASHBOARD_HIGHLIGHTED_SELECTOR,
            name="dashboard highlighted"
        )

    def verify_all_header_icons_visible(self) -> bool:
        """
        Verify that all header icons are visible.
        
        Returns:
            True if all icons are visible
        """
        icon_selectors = [
            self._ICON_NEWSFEED_SELECTOR,
            self._ICON_TODO_SELECTOR,
            self._ICON_USER_PROFILE_SELECTOR,
            self._ICON_TIMESHEETS_SELECTOR,
            self._ICON_NOTIFICATIONS_SELECTOR,
        ]
        for selector in icon_selectors:
            if not self.is_visible(selector, name="header icon"):
                return False
        return True

    # ==================== Search Methods ====================

    def search_by_username(self, username: str) -> None:
        """
        Search for a user by username.
        
        Args:
            username: The username to search for
            
        Raises:
            TimeoutError if search result doesn't appear
        """
        self.type_text(
            self._SEARCH_INPUT_SELECTOR,
            username,
            name="search field"
        )
        self.expect_visible(
            self._FIRST_SEARCH_RESULT_SELECTOR,
            name="first search result"
        )

    def get_search_result_text(self, index: int = 0) -> str:
        """
        Get text content of a search result.
        
        Args:
            index: Index of the result to retrieve (0-based)
            
        Returns:
            Text of the search result
        """
        idx = int(index)
        result_locator = f"{self._SEARCH_RESULTS_SELECTOR}[{idx + 1}]"
        return self.get_text(result_locator, name=f"search result {index}")

    def verify_search_results_contain_keyword(self, keyword: str) -> bool:
        """
        Verify that search results contain the given keyword.
        
        Args:
            keyword: Keyword to search for in results
            
        Returns:
            True if at least one result contains the keyword
        """
        result_count = self.get_count(
            self._SEARCH_RESULTS_SELECTOR,
            name="search results"
        )
        for i in range(result_count):
            result_text = self.get_search_result_text(i)
            if keyword.lower() in result_text.lower():
                return True
        return False

    def click_first_search_result(self) -> None:
        """Click on the first search result."""
        self.force_click(
            self._FIRST_SEARCH_RESULT_SELECTOR,
            name="first search result"
        )

    # ==================== Progress Bar Methods ====================

    def get_invoice_progress_fraction(self) -> str:
        """
        Get invoice progress fraction (e.g., '5/10').
        
        Returns:
            Fraction string
        """
        return self.get_text(
            self._INVOICE_PROGRESS_FRACTION_SELECTOR,
            name="invoice progress fraction"
        )

    def get_invoice_progress_percent(self) -> Optional[str]:
        """
        Get invoice progress percentage value.
        
        Returns:
            Percentage value from data-percent attribute
        """
        return self.get_attribute(
            self._INVOICE_PROGRESS_PERCENT_SELECTOR,
            attribute="data-percent",
            name="invoice progress percent"
        )

    def get_lead_progress_fraction(self) -> str:
        """Get lead progress fraction."""
        return self.get_text(
            self._LEAD_PROGRESS_FRACTION_SELECTOR,
            name="lead progress fraction"
        )

    def get_lead_progress_percent(self) -> Optional[str]:
        """Get lead progress percentage."""
        return self.get_attribute(
            self._LEAD_PROGRESS_PERCENT_SELECTOR,
            attribute="data-percent",
            name="lead progress percent"
        )

    def get_project_progress_fraction(self) -> str:
        """Get project progress fraction."""
        return self.get_text(
            self._PROJECT_PROGRESS_FRACTION_SELECTOR,
            name="project progress fraction"
        )

    def get_project_progress_percent(self) -> Optional[str]:
        """Get project progress percentage."""
        return self.get_attribute(
            self._PROJECT_PROGRESS_PERCENT_SELECTOR,
            attribute="data-percent",
            name="project progress percent"
        )

    def get_task_progress_fraction(self) -> str:
        """Get task progress fraction."""
        return self.get_text(
            self._TASK_PROGRESS_FRACTION_SELECTOR,
            name="task progress fraction"
        )

    def get_task_progress_percent(self) -> Optional[str]:
        """Get task progress percentage."""
        return self.get_attribute(
            self._TASK_PROGRESS_PERCENT_SELECTOR,
            attribute="data-percent",
            name="task progress percent"
        )


