# playwright-robot-android-browserstack

Sample project demonstrating Robot Framework with the [playwright-browserstack](https://pypi.org/project/playwright-browserstack/) library running on real Android devices via BrowserStack Automate.

## Prerequisites

- Python >= 3.9
- A [BrowserStack](https://www.browserstack.com/) account (set `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY`)

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
export BROWSERSTACK_USERNAME=<your_username>
export BROWSERSTACK_ACCESS_KEY=<your_access_key>

robot tests/sample_test.robot
```

## Project Structure

```
libraries/
  PlaywrightAndroidLibrary.py   # Robot Framework keyword library (Playwright Android)
resources/
  android_keywords.robot        # High-level BrowserStack keywords
  variables.robot               # Credentials + device capabilities
tests/
  sample_test.robot             # Sample test suite (The Internet demo site)
output/                         # Robot output artifacts (gitignored)
```

## What the sample tests cover

| Test | Action |
|------|--------|
| Verify Page Title | Navigate to The Internet, assert page title |
| Verify Checkbox Interactions | Check/uncheck checkboxes |
| Verify Dropdown Selection | Select Option 1 from a dropdown |
| Verify Go Back Navigation | Browser back navigation |
| Take Screenshot And Mark Passed | Screenshot + mark BrowserStack session passed |
