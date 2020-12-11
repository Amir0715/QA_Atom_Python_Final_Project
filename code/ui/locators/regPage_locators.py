from selenium.webdriver.common.by import By


class RegPageLocators(object):
    USERNAME_INPUT_LOCATOR = (By.XPATH, '//*[@id="username"]')
    EMAIL_INPUT_LOCATOR = (By.XPATH, '//*[@id="email"]')
    PASSWORD_INPUT_LOCATOR = (By.XPATH, '//*[@id="password"]')
    CONFIRM_PASS_INPUT_LOCATOR = (By.XPATH, '//*[@id="confirm"]')
    TERM_CHECKBOX_LOCATOR = (By.XPATH, '//*[@id="term"]')
    SUBMIT_BUTTON_LOCATOR = (By.XPATH, '//*[@id="submit"]')
