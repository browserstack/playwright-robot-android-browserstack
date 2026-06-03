# Robot Framework with BrowserStack

This sample demonstrates the BrowserStack Python SDK with Robot Framework and Playwright
running on real Android devices via BrowserStack App Automate. The SDK reads
`browserstack.yml`, routes the Playwright session to the Android device platforms defined
there using `playwright.android.connect()`, and reports results to the App Automate
dashboard. No capabilities or CDP URLs are constructed by hand.

> Note: This SDK sample lives alongside the existing (non-SDK) sample in this repository.
> SDK files: `browserstack.yml`, `requirements-sdk.txt`, `sdk_sample_test.robot`,
> `sdk_sample_local_test.robot`, and this `README-SDK.md`.

## Prerequisites

- Python >= 3.9
- Node.js (required by the `robotframework-browser` / Playwright `Browser` library)
- A [BrowserStack](https://www.browserstack.com/) account (username + access key)

## Setup

```bash
git clone https://github.com/browserstack/playwright-robot-android-browserstack.git
cd playwright-robot-android-browserstack

python3 -m venv env
source env/bin/activate          # on Windows: env\Scripts\activate

pip install -r requirements-sdk.txt
rfbrowser init                   # installs the Playwright Node dependencies for the Browser library
```

Set your credentials as environment variables (or edit `userName` / `accessKey` in
`browserstack.yml`):

```bash
export BROWSERSTACK_USERNAME=<your_username>
export BROWSERSTACK_ACCESS_KEY=<your_access_key>
```

## Run Sample Test

```bash
browserstack-sdk robot sdk_sample_test.robot
```

## Run Local Test

```bash
browserstack-sdk robot sdk_sample_local_test.robot
```

## Notes

- This combination (Robot Framework + Playwright on real Android devices via
  `playwright.android.connect()`, routed to App Automate) is newly supported by the SDK and
  should be human-reviewed before publishing.
- View your test results on the [BrowserStack App Automate dashboard](https://app-automate.browserstack.com/).
