login_xpath = {
    "username_textbox": '//input[@name="username"]',
    "password_textbox": '//input[@name="password"]',
    "signin_button": '//input[@name="signInSubmitButton"]'
}

patient_list = {
    "patients_list_div": '//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-6 MuiGrid-grid-md-12 css-zc0b5j"]',
    "add_patient_button": "//button[text() = 'Add Patient']"
}

add_patient = {
    "firstname_textbox": '//div[@class="MuiBox-root css-19kzrtu"]//input[@id="first-name-small"]',
    "lastname_textbox": '//div[@class="MuiBox-root css-19kzrtu"]//input[@id="last-name-small"]',
    "date_field": '//div[@class="MuiBox-root css-19kzrtu"]//input[@id="date"]',
    "gender_dropdown": '//div[@class="MuiBox-root css-19kzrtu"]//div[@id="gender"]',
    "gender_option": '//li[contains(text(), "~")]',  # Male or Female
    "zipcode_textbox": '//div[@class="MuiBox-root css-19kzrtu"]//input[@id="zip"]',
    "mobile_number_textbox": '//div[@class="MuiBox-root css-19kzrtu"]//input[@id="mobile_number"]',
    "address_textbox": '//div[@class="MuiBox-root css-19kzrtu"]//input[@id="address"]',
    "submit_button": '//div[@class="css-x1tq6t"]//button[@type="submit"]',
    "cancel_button": '//div[@class="css-x1tq6t"]//button[@type="reset"]',

    # Patient consent confirmation
    "dialog_box_header": '//h2[@id="alert-dialog-title"]',
    "confirmation_checkbox": '//input[@class="PrivateSwitchBase-input css-1m9pwf3"]',
    "confirm_button": '//button[@class="MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButtonBase-root  css-d2erq6"]',
    "confirmation_cancel_button": '//button[@class="MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeMedium MuiButton-outlinedSizeMedium MuiButtonBase-root  css-18p0rad"]'
}
