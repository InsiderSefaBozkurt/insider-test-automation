# Insider Careers – Selenium Test Suite

End-to-end test automation for the [Insider One](https://useinsider.com) careers hiring funnel,
built with **Python + Selenium 4 + pytest** following the **Page Object Model (POM)** pattern.

---

## Project Structure

```
insider_test/
├── pages/
│   ├── base_page.py              # Shared WebDriver utilities
│   ├── home_page.py              # Insider homepage
│   ├── careers_page.py           # /careers page
│   ├── open_positions_page.py    # Job listings (Lever-powered)
│   └── lever_application_page.py # Lever application form
├── tests/
│   └── test_insider_careers.py   # 6 end-to-end test cases
├── screenshots/                  # Auto-captured on test failure
├── reports/                      # HTML report output
├── conftest.py                   # Fixtures, browser setup, screenshot hook
├── pytest.ini                    # pytest configuration
└── requirements.txt
```

---

## Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Make sure ChromeDriver / GeckoDriver is available in PATH
#    Or use webdriver-manager (already in requirements) – see conftest.py
```

---

## Running Tests

### Chrome (default)
```bash
pytest
```

### Firefox
```bash
pytest --browser=firefox
```

### Single test case
```bash
pytest tests/test_insider_careers.py::TestInsiderCareers::test_01_homepage_is_loaded
```

### With verbose output
```bash
pytest -v
```

---

## Test Cases

| # | Test | Description |
|---|------|-------------|
| TC-01 | `test_01_homepage_is_loaded` | Verify Insider homepage loads |
| TC-02 | `test_02_careers_page_and_explore_button` | Click "We're hiring" → verify Careers page + "Explore open roles" button |
| TC-03 | `test_03_software_development_open_positions` | Click through to Software Development open positions |
| TC-04 | `test_04_filter_by_location_and_team` | Apply Location & Team filters, verify jobs are displayed |
| TC-05 | `test_05_all_jobs_match_filters` | Assert every job matches "Quality Assurance" + "Istanbul, Turkiye" |
| TC-06 | `test_06_apply_redirects_to_lever_form` | Click Apply → verify redirect to Lever application form |

---

## Reports & Screenshots

- **HTML report**: generated at `reports/report.html` after every run.
- **Failure screenshots**: automatically saved to `screenshots/` with timestamp.
