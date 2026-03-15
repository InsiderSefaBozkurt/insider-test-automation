"""
Test Suite: Insider Careers Flow
=================================
  1. Verify the Insider homepage loads.
  2. Navigate to Careers via "We're hiring", verify page + "Explore open roles" button.
  3. Click "Software Development" open positions → verify Lever page loads.
  4. Apply Location + Team filters, verify job listings are displayed.
  5. Validate every listed job contains "Quality Assurance" and "Istanbul, Turkiye".
  6. Click "Apply" → verify redirect to Lever application form.
"""

import pytest
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.open_positions_page import OpenPositionsPage
from pages.lever_application_page import LeverApplicationPage


def _navigate_to_lever_page(driver):
    """
    Navigate from homepage to Lever job listings via Software Development block.
    Returns an OpenPositionsPage instance.
    """
    home = HomePage(driver)
    home.navigate()
    home.click_were_hiring()

    careers = CareersPage(driver)
    careers.click_explore_open_roles()

    positions = OpenPositionsPage(driver)
    positions.click_software_dev_open_positions()

    return positions


class TestInsiderCareers:

    EXPECTED_LOCATION = "Istanbul, Turkiye"
    EXPECTED_TEAM = "Quality Assurance"

    def test_01_homepage_is_loaded(self, driver):
        """TC-01: Verify Insider homepage loads."""
        home = HomePage(driver)
        home.navigate()

        assert home.is_page_loaded(), (
            f"Expected insiderone.com but got: {driver.current_url}"
        )

    def test_02_careers_page_and_explore_button(self, driver):
        """TC-02: Click 'We're hiring' → verify Careers page + 'Explore open roles' button."""
        home = HomePage(driver)
        home.navigate()
        home.click_were_hiring()

        careers = CareersPage(driver)

        assert careers.is_careers_page(), (
            f"Expected careers page but got: {driver.current_url}"
        )
        assert careers.is_explore_open_roles_button_present(), (
            "'Explore open roles' button not found on Careers page."
        )

    def test_03_software_dev_opens_lever_page(self, driver):
        """TC-03: Software Development open positions link → verify Lever page loads."""
        positions = _navigate_to_lever_page(driver)

        assert "lever.co" in driver.current_url, (
            f"Expected jobs.lever.co but got: {driver.current_url}"
        )

    def test_04_filter_by_location_and_team(self, driver):
        """TC-04: Apply Location + Team filters, verify job listings are displayed."""
        positions = _navigate_to_lever_page(driver)

        positions.select_location_filter(self.EXPECTED_LOCATION)
        positions.select_team_filter(self.EXPECTED_TEAM)

        assert positions.are_jobs_displayed(), (
            f"No job listings displayed after filtering by "
            f"Location='{self.EXPECTED_LOCATION}' and Team='{self.EXPECTED_TEAM}'."
        )

    def test_05_all_jobs_match_filters(self, driver):
        """TC-05: Every listed job must contain 'Istanbul, Turkiye' in location."""
        positions = _navigate_to_lever_page(driver)

        positions.select_location_filter(self.EXPECTED_LOCATION)
        positions.select_team_filter(self.EXPECTED_TEAM)

        jobs = positions.get_job_listings()
        assert len(jobs) > 0, "No jobs found after applying filters."

        for job in jobs:
            assert self.EXPECTED_LOCATION.lower() in job["location"].lower(), (
                f"Job '{job['title']}' has location '{job['location']}' "
                f"— expected '{self.EXPECTED_LOCATION}'."
            )

    def test_06_apply_redirects_to_lever_form(self, driver):
        """TC-06: Click Apply → verify redirect to Lever application form."""
        positions = _navigate_to_lever_page(driver)

        positions.select_location_filter(self.EXPECTED_LOCATION)
        positions.select_team_filter(self.EXPECTED_TEAM)

        original_url = driver.current_url
        positions.click_first_apply_button()

        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
        else:
            positions.wait_for_url_changes_from(original_url)

        lever = LeverApplicationPage(driver)
        assert lever.is_lever_application_page(), (
            f"Expected Lever application form but got: {driver.current_url}"
        )

