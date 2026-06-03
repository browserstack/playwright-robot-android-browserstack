*** Settings ***
Documentation       BrowserStack SDK sample test (Robot Framework + Playwright on real
...                 Android devices via App Automate). The BrowserStack SDK reads
...                 browserstack.yml, routes the Playwright session to the Android device
...                 platforms defined there, and reports results to the App Automate
...                 dashboard. No CDP URL or capabilities are built by hand.

Library             Browser


*** Test Cases ***
Add First Product To Cart
    [Documentation]    Open bstackdemo, add the first product to the cart, and assert the
    ...                product name shown in the cart pane matches the listing.
    New Browser    chromium
    New Page    https://bstackdemo.com/
    ${productText}=    Get Text    xpath=//*[@id="1"]/p
    Click    xpath=//*[@id="1"]/div[4]
    Wait For Elements State    css=.float-cart__content    visible
    ${productCartText}=    Get Text
    ...    xpath=//*[@id="__next"]/div/div/div[2]/div[2]/div[2]/div/div[3]/p[1]
    Should Be Equal    ${productCartText}    ${productText}
    Close Browser
