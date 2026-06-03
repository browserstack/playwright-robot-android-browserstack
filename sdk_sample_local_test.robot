*** Settings ***
Documentation       BrowserStack SDK local test (Robot Framework + Playwright on real
...                 Android devices via App Automate). With browserstackLocal: true in
...                 browserstack.yml, the SDK starts the BrowserStack Local tunnel so the
...                 Android device can reach the local endpoint exposed at bs-local.com.

Library             Browser


*** Test Cases ***
Verify Local Page Title
    [Documentation]    Open the BrowserStack Local endpoint and assert the page title.
    New Browser    chromium
    New Page    http://bs-local.com:45454
    ${title}=    Get Title
    Should Be Equal    ${title}    BrowserStack Local
    Close Browser
