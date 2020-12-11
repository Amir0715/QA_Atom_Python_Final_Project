import pytest

from ui.pages.base_page import BasePage
from ui.pages.home_page import HomePage
from ui.pages.reg_page import RegPage


@pytest.fixture()
def base_page(driver):
    return BasePage(driver)


@pytest.fixture()
def reg_page(driver):
    return RegPage(driver)


@pytest.fixture()
def home_page(driver):
    return HomePage(driver)


@pytest.fixture()
def auth(driver):
    page = BasePage(driver)
    page.auth(page.LOGIN, page.PASSWORD)

@pytest.fixture()
def reg(driver, username, email , password):
    page = BasePage(driver)
    page.go_to_reg()
    regPage = RegPage(driver)
    regPage.reg(username, email, password)