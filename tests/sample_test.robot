*** Settings ***
Documentation     Sample Playwright Android test on BrowserStack using Robot Framework.
...               Mirrors browserstack_sample_test.py — tests The Internet demo site.
Library           ../libraries/PlaywrightAndroidLibrary.py
Resource          ../resources/android_keywords.robot
Suite Setup       Connect To BrowserStack Device
Suite Teardown    Disconnect Device
Test Teardown     Run Keyword If Test Failed    Mark Session As Failed    ${TEST NAME} failed


*** Test Cases ***

Verify Page Title
    [Documentation]    Navigate to The Internet and assert the page title.
    Open Chrome On Device
    Set Session Name    playwright-robot-android-sample
    Navigate To    ${BASE_URL}
    Wait For Timeout    3000
    Page Title Should Be    The Internet

Verify Checkbox Interactions
    [Documentation]    Check and uncheck checkboxes on the Checkboxes page.
    Navigate To    ${BASE_URL}
    Click Link    Checkboxes

    # Checkbox 1 starts unchecked — check it
    Checkbox Should Be Unchecked    0
    Check Checkbox    0
    Checkbox Should Be Checked    0

    # Checkbox 2 starts checked — uncheck it
    Checkbox Should Be Checked    1
    Uncheck Checkbox    1
    Checkbox Should Be Unchecked    1

Verify Dropdown Selection
    [Documentation]    Select Option 1 from the dropdown.
    Navigate To    ${BASE_URL}
    Click Link    Dropdown
    Select Option By Label    \#dropdown    Option 1

Verify Go Back Navigation
    [Documentation]    Go back from Dropdown page and verify the heading.
    Navigate To    ${BASE_URL}
    Click Link    Dropdown
    Go Back
    Heading Should Contain    Available Examples    Available Examples

Take Screenshot And Mark Passed
    [Documentation]    Take a screenshot and mark the session as passed.
    Navigate To    ${BASE_URL}
    Take Page Screenshot    output/final_screenshot.png
    Mark Session As Passed    All tests completed successfully
    Close Browser
