import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """Base class for all Page Objects. Provides shared WebDriver utilities."""

    DEFAULT_TIMEOUT = 15

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def open(self, url: str):
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    # ------------------------------------------------------------------
    # Element interactions
    # ------------------------------------------------------------------

    def find(self, by: By, value: str) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_clickable(self, by: By, value: str) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable((by, value)))

    def find_all(self, by: By, value: str):
        self.wait.until(EC.presence_of_all_elements_located((by, value)))
        return self.driver.find_elements(by, value)

    def click(self, by: By, value: str):
        self.find_clickable(by, value).click()

    def click_with_js(self, element: WebElement):
        """JavaScript click – useful for elements blocked by overlays."""
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_into_view(self, element: WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def is_element_present(self, by: By, value: str) -> bool:
        try:
            self.driver.find_element(by, value)
            return True
        except Exception:
            return False

    def wait_for_url_contains(self, partial_url: str, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(partial_url))

    def wait_for_url_changes_from(self, original_url: str, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(EC.url_changes(original_url))

    def switch_to_new_tab(self):
        """Switch driver context to the most recently opened tab."""
        self.wait_for_new_tab()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def wait_for_new_tab(self, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > 1
        )

    # ------------------------------------------------------------------
    # Screenshot
    # ------------------------------------------------------------------

    def take_screenshot(self, name: str = "screenshot") -> str:
        screenshots_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "screenshots"
        )
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(screenshots_dir, f"{name}_{timestamp}.png")
        self.driver.save_screenshot(filepath)
        return filepath
