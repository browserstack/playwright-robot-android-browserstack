*** Variables ***
# BrowserStack credentials — override via CLI: -v BS_USERNAME:myuser
${BS_USERNAME}          %{BROWSERSTACK_USERNAME}
${BS_ACCESS_KEY}        %{BROWSERSTACK_ACCESS_KEY}

# Device capabilities
&{BS_CAPS}
...    deviceName=Samsung Galaxy S23
...    osVersion=13.0
...    browserName=chrome
...    realMobile=true
...    name=playwright-robot-android-sample
...    build=playwright-robot-android

# URLs
${BASE_URL}             https://the-internet.herokuapp.com/
