from ui.locators.regPage_locators import RegPageLocators
from ui.pages.base_page import BasePage


class RegPage(BasePage):

    locators = RegPageLocators()

    def reg(self, username, email, password):
        self.write(self.locators.USERNAME_INPUT_LOCATOR, username)
        self.write(self.locators.EMAIL_INPUT_LOCATOR, email)
        self.write(self.locators.PASSWORD_INPUT_LOCATOR, password)
        self.write(self.locators.CONFIRM_PASS_INPUT_LOCATOR, password)
        self.click(self.locators.TERM_CHECKBOX_LOCATOR)
        self.click(self.locators.SUBMIT_BUTTON_LOCATOR)
