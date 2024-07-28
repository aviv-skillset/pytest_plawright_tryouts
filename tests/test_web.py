"""
This module contains tests for web interactions using Playwright and pytest.
"""

from typing import Generator

import pytest
from playwright.sync_api import Browser, Page, Playwright, sync_playwright


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """
    Fixture to initialize and yield the Playwright instance.
    """
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser_instance(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """
    Fixture to initialize and yield the browser instance.
    """
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page_instance(browser_instance: Browser) -> Generator[Page, None, None]:
    """
    Fixture to initialize and yield a new browser page for each test.
    """
    page = browser_instance.new_page()
    yield page
    page.close()


def test_example(page_instance: Page) -> None:
    """
    Test to check the title of the example.com page.
    """
    page_instance.goto("https://example.com")
    assert "Example Domain" == page_instance.title()


def test_fail(page_instance: Page) -> None:
    """
    Test to check how pytest fails
    """
    page_instance.goto("https://example.com")
    assert "Example Domai" == page_instance.title()
