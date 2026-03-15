import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class OpenPositionsPage(BasePage):
    """
    Page Object for the Insider Careers open positions flow.

    Flow:
      1. careers page → wait for JS to populate href → navigate to Lever
      2. click Location filter button → select "Istanbul, Turkiye"
      3. click Team filter button → select "Quality Assurance"
      4. validate listings
    """

    # ------------------------------------------------------------------
    # Locators – careers page (insiderone.com/careers)
    # ------------------------------------------------------------------

    _SOFTWARE_DEV_LINK = (
        By.CSS_SELECTOR,
        "div[data-department='Software Development'] a.insiderone-icon-cards-grid-item-btn"
    )

    # ------------------------------------------------------------------
    # Locators – Lever job listings page (jobs.lever.co/insiderone)
    # ------------------------------------------------------------------

    # Filter buttons – 2nd and 3rd among filter-button-mlp elements
    _LOCATION_FILTER_BTN = (By.XPATH, "(//div[contains(@class,'filter-button-mlp')])[2]")
    _TEAM_FILTER_BTN = (By.XPATH, "(//div[contains(@class,'filter-button-mlp')])[3]")

    # Filter popup
    _FILTER_POPUP = (By.CSS_SELECTOR, "div.filter-popup")

    # Job posting items
    _JOB_LIST_ITEMS = (By.CSS_SELECTOR, ".posting")
    _JOB_TITLE_CSS = ".posting-name h5"
    _JOB_LOCATION_CSS = ".sort-by-location.location"
    _JOB_DEPARTMENT_CSS = ".posting-categories .department"

    _APPLY_BTN = (By.CSS_SELECTOR, ".posting .posting-btn-submit")

    # ------------------------------------------------------------------
    # Actions – careers page
    # ------------------------------------------------------------------

    def click_software_dev_open_positions(self):
        """Wait until JS populates href, then navigate to Lever."""
        WebDriverWait(self.driver, 20).until(
            lambda d: d.find_element(
                By.CSS_SELECTOR,
                "div[data-department='Software Development'] a.insiderone-icon-cards-grid-item-btn"
            ).get_attribute("href") not in [None, "", "#", "https://insiderone.com/careers/#"]
        )
        link = self.find_clickable(*self._SOFTWARE_DEV_LINK)
        href = link.get_attribute("href")
        self.driver.get(href)

    # ------------------------------------------------------------------
    # Actions – Lever job listings page
    # ------------------------------------------------------------------

    def select_location_filter(self, location: str):
        """Click Location filter button and select the given option."""
        self.find_clickable(*self._LOCATION_FILTER_BTN).click()
        self._wait_for_popup()
        self._click_filter_option(location)
        self._wait_for_jobs_to_reload()

    def select_team_filter(self, team: str):
        """Click Team filter button and select the given option."""
        self.find_clickable(*self._TEAM_FILTER_BTN).click()
        self._wait_for_popup()
        self._click_filter_option(team)
        self._wait_for_jobs_to_reload()

    def _wait_for_popup(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(
                By.XPATH, "//div[contains(@class,'filter-popup') and @style='display: block;']"
            ).is_displayed()
        )

    def _click_filter_option(self, value: str):
        """Click the option link with exact matching text inside the open popup."""
        xpath = f"//div[contains(@class,'filter-popup') and @style='display: block;']//li//a[normalize-space()='{value}']"
        option = self.find_clickable(By.XPATH, xpath)
        option.click()

    def _wait_for_jobs_to_reload(self, timeout: int = 15):
        time.sleep(2)
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self._JOB_LIST_ITEMS)
        )

    # ------------------------------------------------------------------
    # Assertion helpers
    # ------------------------------------------------------------------

    def get_job_listings(self) -> list:
        postings = self.find_all(*self._JOB_LIST_ITEMS)
        jobs = []
        for posting in postings:
            jobs.append({
                "title": self._safe_text(posting, self._JOB_TITLE_CSS),
                "location": self._safe_text(posting, self._JOB_LOCATION_CSS),
                "department": self._safe_text(posting, self._JOB_DEPARTMENT_CSS),
            })
        return jobs

    def _safe_text(self, parent, css_selector: str) -> str:
        try:
            return parent.find_element(By.CSS_SELECTOR, css_selector).text.strip()
        except Exception:
            return ""

    def are_jobs_displayed(self) -> bool:
        return len(self.driver.find_elements(*self._JOB_LIST_ITEMS)) > 0

    def click_first_apply_button(self):
        btn = self.find_clickable(*self._APPLY_BTN)
        self.scroll_into_view(btn)
        btn.click()
