from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators.basePage_locators import BasePageLocators

RETRY_COUNT = 10
TIMEOUT = 20


class BasePage(object):
    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver
        self.LOGIN = 'amir1234'
        self.EMAIL = 'testemail@email.ru'
        self.PASSWORD = '123456'

    def find(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(expected_conditions.presence_of_element_located(locator))

    def click(self, locator, timeout=None):
        for i in range(RETRY_COUNT):
            try:
                self.find(locator)
                element = self.wait(timeout).until(expected_conditions.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i > RETRY_COUNT - 1:
                    raise

    def wait(self, timeout=None):
        if timeout is None:
            timeout = TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    def write(self, locatorInput, keys, isClear=False):
        element = self.find(locatorInput)
        if not isClear:
            element.clear()
        element.send_keys(keys)

    def go_to_reg(self):
        self.click(self.locators.CREATE_ACCOUNT_HREF_LOCATOR)

    def go_to_home(self):
        self.auth(self.LOGIN, self.PASSWORD)

    def auth(self, login, password):
        self.write(self.locators.LOGIN_INPUT_LOCATOR, login)
        self.write(self.locators.PASSWORD_INPUT_LOCATOR, password)
        self.click(self.locators.LOGIN_BUTTON_LOCATOR)

    def check_locator_to_displayed(self, locator, timeout=None, retry_count=RETRY_COUNT):
        for i in range(retry_count):
            try:
                if self.find(locator, timeout).is_displayed():
                    return True
            except TimeoutException:
                if i > retry_count:
                    return False
            except StaleElementReferenceException:
                if i > retry_count:
                    return False
