---
description: "Detailed workflow for generating formatted Test Cases, awaiting User Review, and writing reusable POM-standard Test Scripts with built-in debugging capabilities"
---

# Skill Specification: UI Automation Generator

## Phase 1: Requirements & Visual Processing
- Read and extract logic rules from attached text files (`.md`, `.docx`, `.pdf`) and screenshot images.
- Generate a detailed Test Case list.
- **Step Formatting Rule:** In the "Detailed Step-by-Step Actions" column, every step MUST be formatted on a new line (must have explicit line breaks inside tables):
  
  *Example:*
  1. Navigate to Login Page
  2. Wait for page load to complete
  3. Enter valid credentials
  4. Click Submit button
  5. Wait for Dashboard page to load

- **Page Load Step Policy:** Always include an explicit "Wait for page load" step immediately following any navigation or page-changing action to ensure the DOM is fully loaded before element interactions.

| Test Case ID | Feature / Title | Precondition | Detailed Step-by-Step Actions | Expected Result |
|---|---|---|---|---|

## Phase 2: STOP & Wait for User Confirmation (CRITICAL GATE)
- **DO NOT** scan codebase or write any automation scripts in this turn.
- Immediately after outputting the Test Cases table, append the following prompt to the user:
  > *"Please review the test steps above. Reply with **Confirm** (or request modifications) so I can proceed with scanning the repo and writing the automation scripts."*
- **STOP execution here and wait for the user's reply.**

## Phase 3: Codebase Scanning & Reusability Inspection
*(Executes only AFTER user confirmation)*

1. Identify framework (Playwright, Selenium, Cypress) and programming language.
2. Scan the ENTIRE repository structure to map existing assets for maximum reuse:
   - **Base Page & Wrappers:** Check `base_page` (or base class) for page load wait methods (e.g., `waitForPageLoad()`, `waitForLoadState()`, DOM ready checks), base click/input wrappers, logger instances, and generic wait/error-handling utilities.
   - **Page Objects (`pages/`):** Check all existing Page Object classes for locators or action methods that already exist so they are NOT duplicated.
   - **Fixtures Directory (`fixtures/` or `support/`):** Scan for custom fixtures, context setups, or pre-instantiated page objects.
   - **Utils Directory (`utils/` or `helpers/`):** Scan for logger helpers, screenshot wrappers, wait mechanisms, data generators, and custom wrappers.
3. Match existing coding styles, naming conventions, and setup patterns.
4. Before implementing a test step that needs Page Object behavior, search all relevant Page Object classes and `base_page` for an existing method with the same or equivalent responsibility. Record the reusable method and call it directly when it satisfies the step.

## Phase 4: Page Object & Test Script Code Rules

1. **Reusability First (Zero Duplication):**
   - BEFORE adding any new locator or method, verify if it already exists in `base_page`, existing POM classes, or `utils/`.
   - If an element locator or page action already exists in any file or folder, **reuse it directly**. Do NOT recreate or redefine it.
   - For a required Page Object method, first search by method name and by responsibility (for example, open form, save, search, update, delete, or verify). If an equivalent method exists, reuse it instead of adding a duplicate or a thin wrapper.
   - Add a new method only when no existing method can support the approved test step without weakening clarity or behavior. Keep the method focused on one page action or verification.

2. **Page Object Method Organization:**
   - When adding a new method, identify the functional area it belongs to and place it with related methods rather than appending it arbitrarily.
   - Use clear section comments to classify methods, for example:
     - `# ==================== Create Contract ====================`
     - `# ==================== View Contract ====================`
     - `# ==================== Edit Contract ====================`
     - `# ==================== Delete Contract ====================`
     - `# ==================== Verification ====================`
   - Reuse an existing section comment when the functional area is already present. Add a new section comment only when needed, and keep the naming style consistent with the surrounding Page Object file.
   - If a new method serves a different functional area from the nearby methods, move it to the appropriate section or create the missing section comment so the Page Object remains easy to scan.

3. **Page Load Wait Strategy:**
   - Every page load or major navigation MUST invoke a page-load wait call to ensure DOM readiness before interacting with elements.
   - Re-use the existing page-load wait method from `base_page` (or framework built-ins if no base method exists).

4. **Page Objects & Blank Locators Policy:**
   - Create or update POM classes matching the UI features.
   - For **NEW** locators that do not exist anywhere in the repo, NEVER generate fake XPaths or CSS selectors. Leave locator values empty with a `TODO` comment:
     - *TypeScript:* `private readonly submitButton = page.locator(''); // TODO: Add locator`
     - *Python:* `SUBMIT_BTN = ("", "") # TODO: Add locator strategy and value`

5. **Built-in Debuggability & Observability:**
   - **Descriptive Assertions:** EVERY assertion MUST contain a custom error message explaining what was expected and where it failed.
     - *TypeScript:* `await expect(page.locator('...'), 'Failed at Step 4: Dashboard header should be visible after login').toBeVisible();`
     - *Python:* `assert dashboard.is_header_visible(), "Failed at Step 4: Dashboard header was not visible after login"`
   - **Step Logging & Execution Tracing:** Insert step logs or test annotations (using the project's existing logger or framework step logs like `test.step()` in Playwright / `logging` in Python) before executing critical actions.
     - *Example:* Log `[Step 1] Navigating to Login Page...` before navigation, and `[Action] Clicking Submit Button...` before clicking.
   - **Action Failure Tracing:** Wrap complex or prone-to-fail non-assertion steps (e.g., waiting for popups, iframe switching, dynamic elements) with clear logging/error context so that if a timeout or interaction failure occurs, the logs explicitly state which step, page, or element action failed.

6. **Test Scripts Execution:**
   - Generate test files strictly following the steps approved by the user in Phase 1.
   - Combine page-load waits, step-level logs, descriptive assertions, and reusable methods into a clean, maintainable script structure.