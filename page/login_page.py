from page.base_page import BasePage
from playwright.sync_api import Page, Locator


class LoginPage(BasePage):
    """Page Object Model for login functionality."""

    # ==================== Login Page Locators ====================

    EMAIL = "#email"
    PASSWORD = "#password"
    SUBMIT_BUTTON = "//button[@type='submit']"
    DASHBOARD_MENU = "//li[@class='menu-item-dashboard']//a"
    LOGO = "//div[@id='logo']//a//img"

    # ==================== Initialization ====================

    def __init__(self, page: Page):
        super().__init__(page)

    # ==================== Page Actions ====================
    
    def login(self, username: str, password: str) -> "LoginPage":
        """
        Perform login with provided credentials.
        
        Args:
            username: User email address
            password: User password
            
        Returns:
            LoginPage instance (for method chaining)
            
        Raises:
            TimeoutError: If dashboard doesn't appear after login
        """
        self.fill(self.EMAIL, username, "username")
        self.fill(self.PASSWORD, password, "password")
        self.click(self.SUBMIT_BUTTON, "submit button")
        self.wait_for_load_page()
        self.expect_visible(self.DASHBOARD_MENU, "dashboard")
        return self

    # ==================== Login Verification ====================

    def is_dashboard_visible(self) -> bool:
        """
        Check if dashboard is displayed (indicates successful login).
        
        Returns:
            True if dashboard is visible, False otherwise
        """
        return self.is_visible(self.LOGO, "Anh Tester logo")