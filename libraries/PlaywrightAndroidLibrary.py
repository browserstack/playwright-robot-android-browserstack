"""
Robot Framework keyword library for Playwright Android (BrowserStack).

Usage in .robot files:
    Library    ../libraries/PlaywrightAndroidLibrary.py
"""

import json
import urllib.parse
from playwright.sync_api import sync_playwright, expect


class PlaywrightAndroidLibrary:
    """Playwright Android keywords for Robot Framework."""

    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self):
        self._pw = None
        self._device = None
        self._context = None
        self._page = None

    # ── Connection ────────────────────────────────────────────────────────────

    def connect_to_browserstack(self, username, access_key, caps: dict, timeout=120_000):
        """Connect to a BrowserStack Android device.

        Example:
        | ${caps}=  | Create Dictionary | deviceName=Samsung Galaxy S23 | osVersion=13.0 |
        | Connect To BrowserStack | myuser | mykey | ${caps} |
        """
        caps = dict(caps)
        caps["browserstack.username"] = username
        caps["browserstack.accessKey"] = access_key
        ws_endpoint = (
            "wss://cdp.browserstack.com/playwright?caps="
            + urllib.parse.quote(json.dumps(caps))
        )
        self._pw = sync_playwright().start()
        self._device = self._pw.android.connect(ws_endpoint, timeout=int(timeout))

    def get_device_info(self):
        """Return (serial, model) of the connected device."""
        self._require_device()
        return self._device.serial, self._device.model

    # ── Browser ───────────────────────────────────────────────────────────────

    def launch_browser(self, pkg=None, has_touch=False):
        """Launch Chrome on the device and create a new page.

        Example:
        | Launch Browser |
        | Launch Browser | has_touch=True |
        """
        self._require_device()
        try:
            self._device.shell("am force-stop com.android.chrome")
        except Exception:
            pass
        self._context = self._device.launch_browser(
            pkg=pkg, has_touch=has_touch == "True" or has_touch is True
        )
        self._page = self._context.new_page()

    def close_browser(self):
        """Close the browser context."""
        if self._page:
            self._page.close()
            self._page = None
        if self._context:
            self._context.close()
            self._context = None

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate_to(self, url, timeout=30_000):
        """Navigate to a URL.

        Example:
        | Navigate To | https://example.com |
        """
        self._require_page()
        self._page.goto(url, timeout=int(timeout))

    def go_back(self):
        """Navigate back in browser history."""
        self._require_page()
        self._page.go_back()

    def wait_for_timeout(self, milliseconds):
        """Wait for the given number of milliseconds."""
        self._require_page()
        self._page.wait_for_timeout(int(milliseconds))

    # ── Assertions ────────────────────────────────────────────────────────────

    def page_title_should_be(self, expected_title):
        """Assert the current page title equals the expected value."""
        self._require_page()
        expect(self._page).to_have_title(expected_title)

    def page_title_should_contain(self, text):
        """Assert the current page title contains the given text."""
        self._require_page()
        actual = self._page.title()
        assert text in actual, f"Title {actual!r} does not contain {text!r}"

    def heading_should_contain(self, name, text):
        """Assert a heading with the given name contains text."""
        self._require_page()
        heading = self._page.get_by_role("heading", name=name)
        content = heading.text_content()
        assert text in content, f"Heading text {content!r} does not contain {text!r}"

    # ── Interactions ──────────────────────────────────────────────────────────

    def click_link(self, name):
        """Click a link by its visible text.

        Example:
        | Click Link | Checkboxes |
        """
        self._require_page()
        self._page.get_by_role("link", name=name).click()

    def select_option_by_label(self, selector, label):
        """Select a dropdown option by its visible label.

        Example:
        | Select Option By Label | #dropdown | Option 1 |
        """
        self._require_page()
        self._page.locator(selector).select_option(label=label)

    # ── Checkboxes ────────────────────────────────────────────────────────────

    def checkbox_should_be_unchecked(self, index=0):
        """Assert the Nth checkbox (0-based) is unchecked."""
        self._require_page()
        checkboxes = self._page.get_by_role("checkbox")
        cb = checkboxes.nth(int(index))
        assert not cb.is_checked(), f"Checkbox {index} should be unchecked"

    def checkbox_should_be_checked(self, index=0):
        """Assert the Nth checkbox (0-based) is checked."""
        self._require_page()
        checkboxes = self._page.get_by_role("checkbox")
        cb = checkboxes.nth(int(index))
        assert cb.is_checked(), f"Checkbox {index} should be checked"

    def check_checkbox(self, index=0):
        """Check the Nth checkbox (0-based)."""
        self._require_page()
        self._page.get_by_role("checkbox").nth(int(index)).check()

    def uncheck_checkbox(self, index=0):
        """Uncheck the Nth checkbox (0-based)."""
        self._require_page()
        self._page.get_by_role("checkbox").nth(int(index)).uncheck()

    # ── Screenshot ────────────────────────────────────────────────────────────

    def take_page_screenshot(self, path="screenshot.png"):
        """Save a screenshot of the current page.

        Example:
        | Take Page Screenshot | output/my_test.png |
        """
        self._require_page()
        self._page.screenshot(path=path)

    def take_device_screenshot(self, path="device_screenshot.png"):
        """Save a full-device screenshot.

        Example:
        | Take Device Screenshot | output/device.png |
        """
        self._require_device()
        self._device.screenshot(path=path)

    # ── BrowserStack session status ───────────────────────────────────────────

    def set_session_name(self, name):
        """Set the BrowserStack session name."""
        self._require_page()
        self._page.evaluate(
            "_ => {}",
            f"browserstack_executor: {json.dumps({'action': 'setSessionName', 'arguments': {'name': name}})}",
        )

    def mark_session_as_passed(self, reason="Test passed"):
        """Mark the BrowserStack session as passed."""
        self._set_session_status("passed", reason)

    def mark_session_as_failed(self, reason="Test failed"):
        """Mark the BrowserStack session as failed."""
        self._set_session_status("failed", reason)

    def _set_session_status(self, status, reason):
        self._require_page()
        self._page.evaluate(
            "_ => {}",
            f"browserstack_executor: {json.dumps({'action': 'setSessionStatus', 'arguments': {'status': status, 'reason': reason}})}",
        )

    # ── Teardown ──────────────────────────────────────────────────────────────

    def disconnect_device(self):
        """Close the browser, disconnect the device, and stop Playwright."""
        self.close_browser()
        if self._device:
            self._device.close()
            self._device = None
        if self._pw:
            self._pw.stop()
            self._pw = None

    # ── Internal ──────────────────────────────────────────────────────────────

    def _require_device(self):
        if self._device is None:
            raise RuntimeError("No device connected. Call 'Connect To BrowserStack' first.")

    def _require_page(self):
        if self._page is None:
            raise RuntimeError("No page open. Call 'Launch Browser' first.")
