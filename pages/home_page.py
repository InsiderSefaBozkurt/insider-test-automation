from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for https://useinsider.com → redirects to https://insiderone.com"""

    URL = "https://insiderone.com/"
    EXPECTED_DOMAIN = "insiderone.com"

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    # Cookie consent (OneTrust or similar)
    _COOKIE_ACCEPT_BTN = (By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
    _COOKIE_ACCEPT_BTN_ALT = (By.CSS_SELECTOR, "#wt-cli-accept-all-btn")

    # "Company" nav item – insiderone.com uses a <li> with text "Company"
    # Try multiple selectors for robustness
    _COMPANY_NAV_ITEM = (
        By.XPATH,
        "//nav//a[normalize-space(text())='Company'] | "
        "//nav//span[normalize-space(text())='Company'] | "
        "//ul[contains(@class,'menu')]//li//a[normalize-space()='Company'] | "
        "//header//a[normalize-space()='Company']"
    )

    # "We're hiring" link – may be inside Company submenu or footer
    _WERE_HIRING_LINK = (
        By.XPATH,
        "//*[contains(normalize-space(text()),\"We're hiring\")] | "
        "//*[contains(normalize-space(text()),\"we're hiring\")] | "
        "//a[contains(@href,'career') or contains(@href,'hiring')]"
        "[contains(normalize-space(text()),\"hiring\")]"
    )

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def navigate(self):
        self.open(self.URL)
        self._accept_cookies_if_present()

    def _accept_cookies_if_present(self):
        for locator in [self._COOKIE_ACCEPT_BTN, self._COOKIE_ACCEPT_BTN_ALT]:
            try:
                btn = self.find_clickable(*locator)
                btn.click()
                return
            except Exception:
                continue

    def is_page_loaded(self) -> bool:
        """Verify we are on the Insider One homepage."""
        return self.EXPECTED_DOMAIN in self.get_current_url()

    def click_were_hiring(self):
        """
        Navigate to the Careers / 'We're hiring' page.

        Strategy (most reliable to least):
          1. Hover over 'Company' nav item to reveal submenu, then click link.
          2. Directly click any visible 'We're hiring' anchor.
          3. Navigate directly to the careers URL as a fallback.
        """
        if self._try_company_menu():
            return
        if self._try_direct_were_hiring_link():
            return
        # Fallback: navigate directly
        self.open("https://insiderone.com/careers/")

    def _try_company_menu(self) -> bool:
        """Hover over Company menu item and click 'We're hiring' in the submenu."""
        try:
            import time
            company_item = self.find_clickable(*self._COMPANY_NAV_ITEM)
            self.scroll_into_view(company_item)
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(self.driver).move_to_element(company_item).perform()
            time.sleep(1.5)
            link = self.find_clickable(*self._WERE_HIRING_LINK)
            self.scroll_into_view(link)
            link.click()
            return True
        except Exception:
            return False

    def _try_direct_were_hiring_link(self) -> bool:
        """Click a visible 'We're hiring' link anywhere on the page."""
        try:
            link = self.find_clickable(*self._WERE_HIRING_LINK)
            self.scroll_into_view(link)
            link.click()
            return True
        except Exception:
            return False
