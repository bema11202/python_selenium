#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from assertpy import assert_that
from selenium.webdriver.common.keys import Keys


class TestWebsite:
    # 1. Check browser configuration in browser_setup_and_teardown
    # 2. Run 'Selenium Tests' configuration
    # 3. Test report will be created in reports/ directory

    @pytest.fixture(autouse=True)
    def browser_setup_and_teardown(self):
        """this fixture sets up and tears down browser instance for each test"""
        self.use_selenoid = False  # set to True to run tests with Selenoid

        if self.use_selenoid:
            self.browser = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities={
                    "browserName": "chrome",
                    "browserSize": "1920x1080"
                }
            )
        else:
            self.browser = webdriver.Chrome(
                executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        # self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        self.browser.get("https://www.jetbrains.com/")  # https://www.jetbrains.com/ # https://www.google.com/

        yield

        self.browser.close()
        self.browser.quit()

    def test_tools_menu(self):
        """this test checks presence of Developer Tools menu item"""
        tools_menu = self.browser.find_element(By.XPATH, "//div[@data-test='main-menu-item' and @data-test-marker = 'Developer Tools']")    # find_element_by_xpath(
        tools_menu.click()

        menu_popup = self.browser.find_element(By.CSS_SELECTOR, "div[data-test='main-submenu']")
        assert menu_popup is not None

    def test_navigation_to_all_tools(self):
        """this test checks navigation by See All Tools button"""
        # see_all_tools_button = self.browser.find_element(By.CSS_SELECTOR, "a.wt-button_mode_primary")
        see_all_tools_button = self.browser.find_element(By.XPATH, "//*[text() = 'Developer Tools']")
        see_all_tools_button.click()
        print(self.browser.title)
        # assert self.browser.title == "JetBrains: Essential tools for software developers and teams"
        assert_that(self.browser.find_element(By.CSS_SELECTOR, "div[class ='_mainSubmenu__content_j0qgy _mainSubmenu__content_sq96']").is_displayed())
        assert_that(self.browser.title).is_equal_to("JetBrains: Essential tools for software developers and teams")

    def test_search(self):
        """this test checks search from the main menu"""
        search_button = self.browser.find_element(By.CSS_SELECTOR, "[data-test='site-header-search-action']")
        search_button.click()

        search_field = self.browser.find_element(By.CSS_SELECTOR, "[data-test='search-input']")
        search_field.send_keys("Selenium")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "button[data-test='full-search-button']")
        submit_button.click()

        search_page_field = self.browser.find_element(By.CSS_SELECTOR, "input[data-test='search-input']")
        assert search_page_field.get_property("value") == "Selenium"



