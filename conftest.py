"""
Pytest configuration and fixtures for UI automation tests.
Handles browser setup, authentication, page fixtures, and Allure reporting.
"""

from pathlib import Path
from typing import Dict, Generator, Tuple
import time

import allure
import pytest
import os
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from page.dashboard_page import DashboardPage
from page.customer_page import CustomerPage
from page.contract_page import ContractPage
from page.login_page import LoginPage
from utils import load_json, logger
from utils.allure_helper import AllureHelper
from dotenv import load_dotenv
load_dotenv()

# ==================== Constants ====================
AUTH_FILE = Path("auth/auth.json")
SCREENSHOT_DIR = Path("screenshots")
VIDEO_DIR = Path("videos")
TRACE_DIR = Path("traces")
_AUTH_STATE = None

# Create required directories
SCREENSHOT_DIR.mkdir(exist_ok=True)
VIDEO_DIR.mkdir(exist_ok=True)
TRACE_DIR.mkdir(exist_ok=True)

# Load username and password
BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("ADMIN_EMAIL")
PASSWORD = os.getenv("ADMIN_PASSWORD")

log = logger.get_logger()


# ==================== Session Management ====================
def is_session_valid() -> bool:
    """
    Check if stored authentication session is still valid.
    
    Returns:
        bool: True if a valid non-expired cookie exists, False otherwise
    """
    if not AUTH_FILE.exists():
        return False
    
    try:
        current_time = time.time()
        auth_data = load_json.load_json_file(AUTH_FILE)
        
        for cookie in auth_data.get("cookies", []):
            expires = cookie.get("expires")
            if expires is not None and expires > current_time:
                return True
        return False
    except (FileNotFoundError, ValueError) as e:
        log.warning(f"Error validating session: {e}")
        return False

@pytest.fixture(scope="session")
def ensure_login(browser: Browser):
    global _AUTH_STATE
    if _AUTH_STATE is None:
        log.info("Creating new authentication session")
        # Dùng luôn browser được truyền vào từ fixture, không gọi sync_playwright() ở đây nữa
        context = browser.new_context()
        try:
            page = context.new_page()
            page.goto(BASE_URL)
            LoginPage(page).login(username=USERNAME, password=PASSWORD)
            _AUTH_STATE = context.storage_state()
        finally:
            context.close()
    return _AUTH_STATE

# ==================== Pytest Fixtures ====================
@pytest.fixture(scope="session")
def browser() -> Generator[Browser, None, None]:
    """
    Provide a Playwright browser instance for the entire test session.
    
    Yields:
        Browser: Chromium browser instance
    """
    with sync_playwright() as p:
        browser_instance = p.chromium.launch(headless=True)
        yield browser_instance
        browser_instance.close()


@pytest.fixture
def context(browser: Browser, ensure_login) -> Generator[BrowserContext, None, None]:
    """
    Provide a browser context with authenticated session and video recording.
    
    Args:
        browser: Browser instance from session fixture
        
    Yields:
        BrowserContext: Context with stored authentication and video recording
    """
    # auth_file = ensure_login(browser)
    context_instance = browser.new_context(
        storage_state=ensure_login,
        record_video_dir=str(VIDEO_DIR)
    )
    yield context_instance
    context_instance.close()


@pytest.fixture
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    """
    Provide an authenticated page with tracing enabled.
    
    Args:
        context: Browser context fixture
        request: Pytest request object for test metadata
        
    Yields:
        Page: Playwright page instance
    """
    page_instance = context.new_page()
    trace_path = TRACE_DIR / f"{request.node.name}.zip"
    
    # Store on request for use in hooks
    request.node.trace_path = trace_path
    request.node.page = page_instance
    request.node.context = context
    
    # Start tracing and navigation
    AllureHelper.start_trace(context)
    log.info(f"Navigating to {BASE_URL}")
    page_instance.goto(url=BASE_URL)
    log.info(f"Authenticated as: {USERNAME}")
    
    yield page_instance
    
    # Teardown: stop trace and close page
    AllureHelper.stop_trace(context, trace_path)
    page_instance.close()


# ==================== Page Object Fixtures ====================
@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Fixture to provide LoginPage instance."""
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page: Page) -> DashboardPage:
    """Fixture to provide DashboardPage instance."""
    return DashboardPage(page)


@pytest.fixture
def customer_page(page: Page) -> CustomerPage:
    """Fixture to provide CustomerPage instance."""
    return CustomerPage(page)


@pytest.fixture
def contract_page(page: Page) -> ContractPage:
    """Fixture to provide ContractPage instance."""
    return ContractPage(page)


# ==================== Test Data Fixtures ====================
@pytest.fixture
def search_test_data() -> Dict[str, str]:
    """Test data for search functionality."""
    return {
        "username": "Anh Tester 09072025A2"
    }


@pytest.fixture
def progress_bar_test_data() -> Dict[str, Tuple[str, str]]:
    """
    Test data for progress bar verification.
    
    Returns:
        Dict with keys: invoice, lead, project, task_not_finish
        Each containing tuple of (expected_fraction, expected_percent)
    """
    return {
        "invoice": ("3 / 5", "60.00"),
        "lead": ("02 / 0", "0"),
        "project": ("60 / 67", "89.55"),
        "task_not_finish": ("197 / 197", "100.00"),
    }


# ==================== Pytest Hooks ====================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item) -> None:
    """
    Hook to handle test result reporting and artifact attachment.
    Captures screenshots, logs, videos, and traces on test failure.
    
    Args:
        item: Pytest test item
    """
    outcome = yield
    report = outcome.get_result()
    
    # Store report for later use
    setattr(item, f"report_{report.when}", report)
    
    # Handle test failure (call phase)
    if report.when == "call" and report.failed:
        _handle_test_failure(item)
    
    # Handle teardown phase - attach video if exists
    if report.when == "teardown":
        _attach_video_if_exists(item)
    
    # Handle trace attachment
    if report.when == "call":
        _attach_trace_if_exists(item)


def _handle_test_failure(item: pytest.Item) -> None:
    """
    Attach artifacts (screenshot and log) when test fails.
    
    Args:
        item: Pytest test item
    """
    page = item.funcargs.get("page")
    
    if page:
        screenshot_path = SCREENSHOT_DIR / f"{item.name}.png"
        page.screenshot(path=screenshot_path)
        AllureHelper.attach_screenshot(screenshot_path)
        log.error(f"Test failed. Screenshot saved: {screenshot_path}")
    
    log_path = logger.LOG_FILE
    AllureHelper.attach_log(log_path)


def _attach_video_if_exists(item: pytest.Item) -> None:
    """
    Attach video recording if it exists.
    
    Args:
        item: Pytest test item
    """
    # Video path is stored during context teardown
    video_path = getattr(item, "video_path", None)
    
    if video_path and Path(video_path).exists():
        AllureHelper.attach_video(video_path)


def _attach_trace_if_exists(item: pytest.Item) -> None:
    """
    Attach trace file if it exists.
    
    Args:
        item: Pytest test item
    """
    trace_path = getattr(item, "trace_path", None)
    
    if trace_path and trace_path.exists():
        AllureHelper.attach_trace(trace_path)