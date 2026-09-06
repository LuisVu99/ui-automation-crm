from playwright.sync_api import Page, expect, Locator, TimeoutError
from typing import Optional, Union
import logging
from pathlib import Path
from urllib.parse import urljoin
import os

# Configure logging
logger = logging.getLogger(__name__)

class BasePage:
    """
    Base page class providing robust wrapper methods for Playwright automation.
    Includes built-in explicit waits and error handling to minimize flakiness.
    """

    # ==================== Configuration and Initialization ====================

    # Default timeout for operations (milliseconds)
    DEFAULT_TIMEOUT = 30000  # 30 seconds
    
    def __init__(self, page: Page, base_url: Optional[str] = None):
        """
        Initialize BasePage with Playwright Page object.
        
        Args:
            page: Playwright Page instance
            base_url: Optional base URL for navigation
        """
        self.page: Page = page
        self.base_url: Optional[str] = base_url or os.getenv("BASE_URL")
        logger.info(f"Initialized {self.__class__.__name__}")

    # ==================== Navigation Methods ====================
    
    def navigate(self, url: str) -> None:
        """
        Navigate to a specific URL.
        
        Args:
            url: The URL to navigate to (absolute or relative if base_url is set)
        """
        full_url = urljoin(f"{self.base_url.rstrip('/')}/", url.lstrip("/"))
        logger.info(f"Navigating to: {full_url}")
        self.page.goto(full_url, wait_until="networkidle")
    
    def navigate_and_wait(self, url: str, wait_for_locator: str) -> None:
        """
        Navigate to URL and wait for a specific element to be visible.
        
        Args:
            url: The URL to navigate to
            wait_for_locator: Locator string to wait for
        """
        logger.info(f"Navigating to {url} and waiting for {wait_for_locator}")
        self.navigate(url)
        self.wait_for_selector(wait_for_locator)
    
    # ==================== Click Methods ====================
    
    def click(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Click on an element with explicit wait.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Clicking: {name or locator}")
        try:
            self.page.locator(locator).click(timeout=timeout)
        except TimeoutError:
            logger.error(f"Failed to click '{name}' - element not found or not clickable")
            raise
    
    def click_and_wait_for_navigation(self, locator: str, name: str = "") -> None:
        """
        Click element and wait for navigation to complete.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
        """
        logger.info(f"Clicking '{name}' and waiting for navigation")
        with self.page.expect_navigation():
            self.click(locator, name)
    
    def force_click(self, locator: str, name: str = "") -> None:
        """
        Force click on element (bypasses visibility checks).
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
        """
        logger.info(f"Force clicking: {name or locator}")
        self.page.locator(locator).click(force=True)
    
    # ==================== Fill/Input Methods ====================
    
    def fill(self, locator: str, text: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Clear and fill a text input field.
        
        Args:
            locator: CSS/XPath selector
            text: Text to fill
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Filling '{name or locator}' with: {text}")
        try:
            self.page.locator(locator).fill(text, timeout=timeout)
        except TimeoutError:
            logger.error(f"Failed to fill '{name}' - element not found or not accessible")
            raise
    
    def clear(self, locator: str, name: str = "") -> None:
        """
        Clear a text input field.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
        """
        logger.info(f"Clearing: {name or locator}")
        self.page.locator(locator).clear()
    
    def type_text(self, locator: str, text: str, name: str = "", delay: int = 100) -> None:
        """
        Type text character by character with delay.
        
        Args:
            locator: CSS/XPath selector
            text: Text to type
            name: Description for logging
            delay: Delay between keystrokes in milliseconds
        """
        logger.info(f"Typing in '{name or locator}': {text}")
        self.page.locator(locator).type(text, delay=delay)
    
    # ==================== Visibility/Wait Methods ====================
    
    def is_visible(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> bool:
        """
        Check if element is visible with timeout.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            True if visible, False otherwise
        """
        logger.info(f"Checking visibility of: {name or locator}")
        try:
            return self.page.locator(locator).is_visible(timeout=timeout)
        except TimeoutError:
            logger.info(f"Element '{name}' is not visible")
            return False
    
    def expect_visible(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Assert that element is visible (fails test if not).
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Expecting visible: {name or locator}")
        expect(self.page.locator(locator)).to_be_visible(timeout=timeout)
    
    def expect_hidden(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Assert that element is hidden (fails test if visible).
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Expecting hidden: {name or locator}")
        expect(self.page.locator(locator)).to_be_hidden(timeout=timeout)
    
    def wait_for_selector(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> Locator:
        """
        Wait for element to be present in DOM.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            Locator object if found
        """
        logger.info(f"Waiting for selector: {name or locator}")
        return self.page.locator(locator).first.wait_for(state="attached", timeout=timeout)
    
    def wait_for_element_hidden(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Wait for element to be hidden.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Waiting for element to be hidden: {name or locator}")
        self.page.locator(locator).wait_for(state="hidden", timeout=timeout)

    def wait_for_load_page(self, timeout: int = DEFAULT_TIMEOUT) -> None:
            """
            Wait for page load successfully.
            
            Args:
                name: Wait for page load
                timeout: Maximum time to wait in milliseconds
            """
            logger.info(f"Waiting for page load")
            self.page.wait_for_load_state(state="networkidle", timeout=timeout)

    # ==================== Text Methods ====================
    
    def get_text(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> str:
        """
        Get visible text content from element.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            Text content
        """
        logger.info(f"Getting text from: {name or locator}")
        text = self.page.locator(locator).inner_text(timeout=timeout).strip()
        logger.debug(f"Retrieved text: {text}")
        return text
    
    def get_input_value(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> str:
        """
        Get value from input field.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            Input value
        """
        logger.info(f"Getting input value from: {name or locator}")
        return self.page.locator(locator).input_value(timeout=timeout)
    
    # ==================== Attribute Methods ====================
    
    def get_attribute(self, locator: str, attribute: str, name: str = "", 
                      timeout: int = DEFAULT_TIMEOUT) -> Optional[str]:
        """
        Get attribute value from element.
        
        Args:
            locator: CSS/XPath selector
            attribute: Attribute name
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            Attribute value or None
        """
        logger.info(f"Getting attribute '{attribute}' from: {name or locator}")
        return self.page.locator(locator).get_attribute(attribute, timeout=timeout)
    
    def has_attribute(self, locator: str, attribute: str, value: str = None) -> bool:
        """
        Check if element has an attribute (optionally with specific value).
        
        Args:
            locator: CSS/XPath selector
            attribute: Attribute name
            value: Optional expected value
            
        Returns:
            True if attribute exists (and matches value if provided)
        """
        attr_value = self.get_attribute(locator, attribute)
        if attr_value is None:
            return False
        return value is None or attr_value == value

    # ==================== Interaction Methods ====================
    
    def hover(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Hover over element.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Hovering over: {name or locator}")
        self.page.locator(locator).hover(timeout=timeout)
    
    def double_click(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Double click on element.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Double clicking: {name or locator}")
        self.page.locator(locator).dblclick(timeout=timeout)
    
    def right_click(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Right click (context menu) on element.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Right clicking: {name or locator}")
        self.page.locator(locator).click(button="right", timeout=timeout)
    
    def scroll_into_view(self, locator: str, name: str = "") -> None:
        """
        Scroll element into view.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
        """
        logger.info(f"Scrolling into view: {name or locator}")
        self.page.locator(locator).scroll_into_view_if_needed()
    
    # ==================== Dropdown/Select Methods ====================
    
    def select_option(self, locator: str, value: Union[str, int], name: str = "", 
                      timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Select option in dropdown.
        
        Args:
            locator: CSS/XPath selector
            value: Option value or index
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Selecting option '{value}' from: {name or locator}")
        self.page.locator(locator).select_option(str(value), timeout=timeout)
    
    def get_selected_option(self, locator: str, name: str = "", 
                            timeout: int = DEFAULT_TIMEOUT) -> str:
        """
        Get currently selected option value.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            Selected option value
        """
        logger.info(f"Getting selected option from: {name or locator}")
        return self.page.locator(locator).input_value(timeout=timeout)
    
    # ==================== Checkbox/Radio Methods ====================
    
    def check(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Check a checkbox or radio button.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Checking: {name or locator}")
        self.page.locator(locator).check(timeout=timeout)
    
    def uncheck(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Uncheck a checkbox.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Unchecking: {name or locator}")
        self.page.locator(locator).uncheck(timeout=timeout)
    
    def is_checked(self, locator: str, name: str = "", timeout: int = DEFAULT_TIMEOUT) -> bool:
        """
        Check if checkbox/radio is checked.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            True if checked
        """
        logger.info(f"Checking if checked: {name or locator}")
        return self.page.locator(locator).is_checked(timeout=timeout)

    # ==================== List/Count Methods ====================
    
    def get_count(self, locator: str, name: str = "") -> int:
        """
        Get count of elements matching locator.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            
        Returns:
            Number of matching elements
        """
        logger.info(f"Getting count of: {name or locator}")
        return self.page.locator(locator).count()
    
    def get_all_text(self, locator: str, name: str = "") -> list[str]:
        """
        Get text from all matching elements.
        
        Args:
            locator: CSS/XPath selector
            name: Description for logging
            
        Returns:
            List of text content
        """
        logger.info(f"Getting all text from: {name or locator}")
        elements = self.page.locator(locator)
        return [elements.nth(i).inner_text().strip() for i in range(elements.count())]

    # ==================== Utility Methods ====================
    
    def execute_script(self, script: str, arg: Optional[any] = None) -> any:
        """
        Execute JavaScript in page context.
        
        Args:
            script: JavaScript code
            arg: Optional argument to pass to script
            
        Returns:
            Script return value
        """
        logger.info(f"Executing script")
        return self.page.evaluate(script, arg)
    
    def take_screenshot(self, name: str = "screenshot.png", path: str = "screenshots") -> str:
        """
        Take screenshot and save to file.
        
        Args:
            name: Screenshot filename
            path: Directory to save screenshot
            
        Returns:
            Full file path
        """
        Path(path).mkdir(parents=True, exist_ok=True)
        file_path = f"{path}/{name}"
        logger.info(f"Taking screenshot: {file_path}")
        self.page.screenshot(path=file_path)
        return file_path
    
    def accept_alert(self) -> str:
        """Accept browser alert and return its message."""
        logger.info("Accepting alert")
        return self.page.on("dialog", lambda dialog: dialog.accept())
    
    def dismiss_alert(self) -> str:
        """Dismiss browser alert and return its message."""
        logger.info("Dismissing alert")
        return self.page.on("dialog", lambda dialog: dialog.dismiss())
    
    def wait_for_url(self, url_pattern: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Wait for page URL to match pattern.
        
        Args:
            url_pattern: URL pattern (supports wildcards)
            timeout: Maximum time to wait in milliseconds
        """
        logger.info(f"Waiting for URL: {url_pattern}")
        self.page.wait_for_url(url_pattern, timeout=timeout)
    
    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            Current URL
        """
        return self.page.url