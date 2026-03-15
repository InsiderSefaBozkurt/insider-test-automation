from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LeverApplicationPage(BasePage):
    """Page Object for the Lever job application form."""

    EXPECTED_URL_FRAGMENT = "jobs.lever.co"

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    _APPLICATION_FORM = (By.CSS_SELECTOR, "form.application-form")
    _APPLY_HEADING = (By.CSS_SELECTOR, "h2.apply-section-header")

    # ------------------------------------------------------------------
    # Assertion helpers
    # ------------------------------------------------------------------

    def is_lever_application_page(self) -> bool:
        """Return True when the driver is on a Lever application form page."""
        return self.EXPECTED_URL_FRAGMENT in self.get_current_url()
