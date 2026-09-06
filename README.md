# CRM UI Test Automation

Python and Playwright test automation framework for validating the CRM web application's authentication and dashboard experience. The project uses Pytest for test execution, Page Object Model classes for maintainable UI interactions, and Allure for test reporting and failure artifacts.

## Project Overview

End-to-end CRM UI tests cover authentication, dashboard visibility/search, navigation, widgets, header icons, and progress-bar values. Playwright failure screenshots, videos, traces, and logs are attached to Allure where supported.

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python 3.11 | Test automation language and CI runtime |
| Playwright | Browser automation and Chromium execution |
| Pytest | Test runner, fixtures, parametrization, and markers |
| `pytest-playwright` | Pytest integration for Playwright |
| Allure Report | Test results, steps, metadata, and failure evidence |
| GitHub Actions | Continuous integration and scheduled test execution |
| `python-dotenv` | Loading local environment variables from `.env` |
| `pytest-xdist` | Parallel test execution support |
| Faker / `jsonschema` / PyYAML | Test-data and utility dependencies available to the framework |

## Project Structure

```text
.
├── .env_example                 # Environment-variable template
├── .github/
│   ├── agents/ui-automation.agent.md # AI test-generation agent
│   ├── skills/ui-test-skill.md       # AI test-generation rules
│   └── workflows/playwright.yml      # CI and Allure pipeline
├── config/
│   └── environments.json        # Example environment definitions
├── data/
│   └── dashboard_data.json      # Dashboard test data
├── page/                         # Base class and Page Objects
├── tests/                        # Pytest UI tests
├── utils/                        # Allure, JSON, and logging helpers
├── conftest.py                  # Browser, authentication, page, and hooks
├── pytest.ini                   # Pytest defaults
├── requirements.txt              # Python dependencies
├── allure-results/              # Generated raw Allure results (ignored)
├── allure-report/               # Generated HTML report (ignored)
├── screenshots/                 # Failure screenshots (ignored)
├── videos/                      # Recorded browser videos (ignored)
├── traces/                      # Playwright trace ZIP files (ignored)
└── logs/                        # Automation logs (ignored)
```

Artifact directories are generated during test runs. Authentication state is stored under `auth/` and is excluded from version control.

## AI Agent & Skill Workflow

Use the `ui-automation` agent with `.github/skills/ui-test-skill.md` to turn requirements into POM-based tests. The agent must stop after test-case generation and wait for `Confirm` before inspecting code or editing files.

### Quick workflow

1. **Prepare:** Put requirements in `documents/crm/`; provide the feature, role, test data, acceptance criteria, and UI files. Never include secrets or real customer data.
2. **Generate cases:** Ask for a table with Test Case ID, title, precondition, step-by-step actions, and expected result. Put each action on a new line and add a page-load wait after navigation.
3. **Review:** Check happy path, validation/boundary, permissions, expected errors, data dependencies, and duplicates. Reply `Confirm` only when the cases are correct.
4. **Inspect and reuse:** After `Confirm`, search `base_page`, Page Objects, `conftest.py`, `utils/`, `data/`, and nearby tests before adding methods or locators. Add methods only when no equivalent exists; group them under `Create`, `View`, `Edit`, `Delete`, or `Verification`.
5. **Implement:** Keep locators/actions in Page Objects. Use page-load waits, descriptive assertion messages, Allure/logger steps, fixtures or parametrization, and no credentials in code. Leave unconfirmed new locators as `TODO` until QA verifies them in the DOM.
6. **Validate:** Confirm locators, run the focused test, inspect failure artifacts, then run related markers and the full suite. Review the diff and Allure results before merging.

Example first prompt:

```text
Read documents/crm/requirements_contracts.md and the attached UI images.
Create test cases for [feature], including happy path, validation, boundary,
and permission scenarios. Only return the test-case table and wait for my
review; do not inspect the codebase or write scripts yet.
```

### New test checklist

- Requirements and acceptance criteria are clear.
- Test cases are reviewed and confirmed before coding.
- Existing Page Objects, fixtures, utilities, and data were searched first.
- Navigation waits, strong assertions, logging, and Allure steps are present.
- Test data is repeatable and contains no secrets.
- The focused test, related marker, and final suite pass.

### Resume after a long break

Check `.env`, read the relevant file in `documents/crm/`, open the agent and skill, inspect the nearest test/Page Object/fixture, then run one focused test. For a new feature, restart at step 1; do not skip the `Confirm` gate. AI proposes code, but the reviewer validates requirements, locators, data, permissions, and pass/fail results.

## Local Setup & Configuration

Prerequisites: Python 3.11+, Git, Node.js/npm and Java for the Allure CLI.

### 1. Create the environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies and browsers

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install --with-deps
```

The browser fixture launches Chromium in headless mode.

### 3. Configure environment variables

Copy the template and replace its placeholder values with credentials for a non-production test account:

```powershell
Copy-Item .env_example .env
```

The test runtime currently reads these variables from `.env`:

| Variable | Required by current tests | Description |
| --- | --- | --- |
| `BASE_URL` | Yes | CRM URL used for navigation and login |
| `ADMIN_EMAIL` | Yes | Administrator email used during session setup |
| `ADMIN_PASSWORD` | Yes | Administrator password used during session setup |

Other variables in `.env_example` are reserved for future role/environment scenarios; the current login flow uses only `BASE_URL`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD`.

Do not commit `.env` or real credentials. The repository ignore rules exclude local environment files and sensitive authentication data.

> **Configuration note:** `.env_example` defines environment-specific URL names, while the executable test code expects `BASE_URL`. Set `BASE_URL` explicitly in `.env`. The CI workflow currently maps the GitHub Repository/Environment **Variable** named `BASE_URL` to that runtime variable.

## Running Tests Locally

```bash
pytest --clean-alluredir --alluredir=allure-results tests
```

Focused test and verbose output:

```bash
pytest tests\test_<feature>.py -v --tb=short --alluredir=allure-results
```

Run a subset using the current Pytest markers:

```bash
pytest -m smoke --alluredir=allure-results
pytest -m regression --alluredir=allure-results
pytest -m "ui and functional" --alluredir=allure-results
```

Failure artifacts are written to `screenshots/`, `videos/`, `traces/`, and `logs/automation.log`.

### View the Allure report locally

Serve the results locally after installing the Allure CLI:

```bash
allure serve allure-results
```

To generate a reusable report directory:

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

## CI/CD Pipeline: GitHub Actions

`.github/workflows/playwright.yml` runs on Ubuntu with Python 3.11, installs dependencies and browsers, runs Pytest, publishes raw results, generates Allure, and deploys the report to `gh-pages`.

Triggers: pull requests and pushes to `master`, `v*` tags, releases, manual `workflow_dispatch`, and schedule `0 0 * * 2,4,6` UTC.

### Required GitHub configuration

Configure these in the `developer` Environment:

| Name | Type | Required | Used by |
| --- | --- | --- | --- |
| `BASE_URL` | Variable | Yes | Target CRM URL passed to Pytest |
| `ADMIN_EMAIL` | Secret | Yes | Administrator login email |
| `ADMIN_PASSWORD` | Secret | Yes | Administrator login password |
| `GITHUB_TOKEN` | Automatic secret | Yes | Publishing the report to `gh-pages` |

The checked-in workflow uses `vars.BASE_URL`, not `vars.REPO_BASE_URL`, and currently authenticates with admin credentials only. Add user credentials as Environment Secrets only when user-role tests are implemented. Never store passwords in Variables or source files.

### Pipeline stages and report

Enable GitHub Pages for the repository and select the `gh-pages` branch as the publishing source. After a successful workflow run, open:

```text
https://<github-owner>.github.io/<repository-name>/
```

Replace the placeholders with the repository values. The workflow also retains `allure-report` as an Actions artifact.

## Maintenance Notes

- Keep selectors and page actions inside the relevant Page Object class.
- Keep secrets in local `.env` files or GitHub Secrets; do not commit authentication state.
- Update expected dashboard values in the test parametrization when the test environment's legitimate data changes.
- Preserve Allure history on `gh-pages` so trend information is retained between pipeline runs.