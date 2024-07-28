"""
This module contains tests for web interactions using Playwright and pytest.
"""

import re
from typing import Generator

import pytest
from playwright.sync_api import Browser, Page, Playwright, expect, sync_playwright


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
    browser = playwright_instance.chromium.launch(
        headless=False,
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser_instance: Browser) -> Generator[Page, None, None]:
    """
    Fixture to initialize and yield a new browser page for each test.
    """
    page = browser_instance.new_page()
    yield page
    page.close()


def test_example(page: Page) -> None:
    """
    Test to check the title of the example.com page.
    """
    page.goto("https://example.com")
    assert "Example Domain" == page.title()


def test_has_title(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))


def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()


@pytest.mark.xfail(reason="intentional fail")
def test_fail(page: Page) -> None:
    """
    Test to check how pytest fails
    """
    page.goto("https://example.com")
    assert "Example Domai" == page.title()
