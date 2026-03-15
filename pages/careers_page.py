from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CareersPage(BasePage):
    """Page Object for the Insider Careers page."""

    # insiderone.com careers URL
    EXPECTED_URL_FRAGMENTS = ["insiderone.com/careers"]

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    # "Explore open roles" button – try multiple text variants
    _EXPLORE_OPEN_ROLES_BTN = (
        By.XPATH,
        "//a[normalize-space()='Explore open roles'] | "
        "//a[normalize-space()='Explore Open Roles'] | "
        "//a[contains(normalize-space(),'Explore') and contains(normalize-space(),'roles')] | "
        "//a[contains(normalize-space(),'Explore') and contains(normalize-space(),'Roles')]"
    )

    # ------------------------------------------------------------------
    # Assertions helpers
    # ------------------------------------------------------------------

    def is_careers_page(self) -> bool:
        """Return True when current URL matches the careers page."""
        current = self.get_current_url()
        return any(fragment in current for fragment in self.EXPECTED_URL_FRAGMENTS)

    def is_explore_open_roles_button_present(self) -> bool:
        return self.is_element_present(*self._EXPLORE_OPEN_ROLES_BTN)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def click_explore_open_roles(self):
        btn = self.find_clickable(*self._EXPLORE_OPEN_ROLES_BTN)
        self.scroll_into_view(btn)
        btn.click()
