*** Settings ***
Library     ../libraries/PlaywrightAndroidLibrary.py
Resource    variables.robot


*** Keywords ***
Connect To BrowserStack Device
    [Documentation]    Open a BrowserStack Android session using suite-level caps.
    Connect To BrowserStack    ${BS_USERNAME}    ${BS_ACCESS_KEY}    ${BS_CAPS}
    ${serial}    ${model}=    Get Device Info
    Log    Connected: serial=${serial} model=${model}

Open Chrome On Device
    [Documentation]    Launch Chrome and open a blank page.
    Launch Browser

Open Chrome With Touch On Device
    [Documentation]    Launch Chrome with touch enabled (required for touchscreen.tap).
    Launch Browser    has_touch=True

Teardown Session
    [Arguments]    ${status}=${TEST STATUS}    ${msg}=${TEST MESSAGE}
    [Documentation]    Mark session status, screenshot, then disconnect.
    Run Keyword If    '${status}' == 'PASS'
    ...    Mark Session As Passed    ${msg}
    ...    ELSE    Mark Session As Failed    ${msg}
    Take Page Screenshot    output/${TEST NAME}.png
    Disconnect Device
