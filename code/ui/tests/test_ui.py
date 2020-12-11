from selenium.webdriver import ActionChains

from functions.rand_user import create_user
from ui.fixtures.pageObject_fixtures import *
from ui.tests.base import BaseCase


class TestUI(BaseCase):


    @pytest.fixture(scope='function')
    def user(self):
        username, email, password = create_user()
        user = self.MySqlBuilder.add_user(username=username, email=email, password=password, access=1, active=0)
        yield username, password, email
        self.MySqlBuilder.del_user(username)

    @pytest.fixture(scope='function')
    def blocked_user(self):
        username, email, password = create_user()
        user = self.MySqlBuilder.add_user(username=username, email=email, password=password, access=0, active=0)
        yield username, password, email
        self.MySqlBuilder.del_user(username)

    @pytest.mark.UI
    def test_auth(self, user):
        """
            Тестируется авторизация пользователя через UI .
            Шаги:
            1. Создается пользователь через базу данных.
            2. Происходит авторизация через форму.
            Ожидается имя пользователя на главной странице.
        """
        username, password, email = user
        self.base_page.auth(username, password)
        assert username in self.driver.page_source

    @pytest.mark.UI
    def test_auth_via_blocked_user(self, blocked_user):
        """
            Тестируется авторизация заблокированного пользователя через UI .
            Шаги:
            1. Создается заблокированный пользователь через базу данных.
            2. Происходит авторизация через форму.
            Ожидается что авторизация не пройдет.
        """
        username, password, email = blocked_user
        self.base_page.auth(username, password)
        assert 'Ваша учетная запись заблокирована' in self.driver.page_source

    @pytest.mark.UI
    def test_negative_auth(self):
        """
            Тестируется авторизация несуществующего пользователя через UI .
            Шаги:
            1. Происходит авторизация через форму.
            Ожидается что авторизация не пройдет.
        """
        self.base_page.auth('dajsdja', 'fwikfbdas')
        assert 'Invalid username or password' in self.driver.page_source

    @pytest.mark.UI
    def test_reg(self):
        """
            Тестируется регистрация пользователя через UI .
            Шаги:
            1. Происходит регистрация через форму.
            Ожидается что регистрация пройдет.
        """
        self.base_page.go_to_reg()
        self.reg_page.reg('amir0715', 'amir@test.ru', '123456')
        assert 'Logged as amir0715' in self.driver.page_source
        self.MySqlBuilder.del_user('amir0715')

    @pytest.mark.UI
    def test_negative_reg(self):
        """
            Тестируется регистрация существуещего пользователя через UI .
            Шаги:
            1. Происходит регистрация через форму.
            2. Выход из аккаунта.
            3. Происходит регистрация через форму.
            Ожидается что регистрация не пройдет.
        """
        self.base_page.go_to_reg()
        self.reg_page.reg('amir0715', 'amir@test.ru', '123456')
        self.home_page.click(self.home_page.locators.LOGOUT_BUTTON_LOCATOR)
        self.base_page.go_to_reg()
        self.reg_page.reg('amir0715', 'amir@test.ru', '123456')
        assert 'User already exist' in self.driver.page_source

    @pytest.mark.UI
    def test_what_is_an_api(self, user):
        """
            Тестируется ссылка на главной страницу через UI .
            Шаги:
            1. Создается пользователь через базу данных.
            2. Переходим по ссылке.
            Ожидается что ссылка введет на сайт о апи.
        """
        username, password, _ = user
        self.base_page.auth(username, password)
        self.home_page.click(self.home_page.locators.API_HREF_LOCATOR)
        self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
        assert 'API' in self.driver.page_source

    @pytest.mark.UI
    def test_internet(self, user):
        """
            Тестируется ссылка на главной страницу через UI .
            Шаги:
            1. Создается пользователь через базу данных.
            2. Переходим по ссылке.
            Ожидается что ссылка введет на сайт об интернете.
        """
        username, password, _ = user
        self.base_page.auth(username, password)
        self.home_page.click(self.home_page.locators.INTERNET_HREF_LOCATOR)
        self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
        assert 'What Will the Internet Be Like in the Next 50 Years?' in self.driver.page_source

    @pytest.mark.UI
    def test_smtp(self, user):
        """
            Тестируется ссылка на главной страницу через UI .
            Шаги:
            1. Создается пользователь через базу данных.
            2. Переходим по ссылке.
            Ожидается что ссылка введет на сайт о почтовом протоколе.
        """
        username, password, _ = user
        self.base_page.auth(username, password)
        self.home_page.click(self.home_page.locators.SMTP_HREF_LOCATOR)
        self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
        assert 'SMTP' in self.driver.page_source

    @pytest.mark.UI
    @pytest.mark.parametrize('LOCATORS', [
        ['HOME_MENU_LOCATOR', 'powered by ТЕХНОАТОМ', 'HOME_MENU_LOCATOR'],
        ['PYTHON_MENU_LOCATOR', 'Python is a programming language that lets you work quickly', 'PYTHON_MENU_LOCATOR'],
        ['PYTHON_HISTORY_MENU_LOCATOR', 'History of Python', 'PYTHON_MENU_LOCATOR'],
        ['PYTHON_FLASK_MENU_LOCATOR', 'User’s Guide', 'PYTHON_MENU_LOCATOR'],
        ['LINUX_FEDORA_MENU_LOCATOR', 'Загрузить Fedora', 'LINUX_MENU_LOCATOR'],
        ['NETWORK_WIRESHARK_NEWS_MENU_LOCATOR', 'Wireshark 3.4.0 and 3.2.8 Released', 'NETWORK_MENU_LOCATOR'],
        ['NETWORK_WIRESHARK_DOWNLOAD_MENU_LOCATOR', 'Download Wireshark', 'NETWORK_MENU_LOCATOR'],
        ['NETWORK_TCPDUMP_MENU_LOCATOR', 'Tcpdump Examples', 'NETWORK_MENU_LOCATOR'],
    ])
    def test_menu(self, LOCATORS, user):
        """
            Тестируются кнопки меню на главной страницу через UI .
            Шаги:
            1. Создается пользователь через базу данных.
            2. Переходим по ссылке.
            Ожидается что ссылка введет на сайт с локатором <LOCATORS>.
        """
        username, password, _ = user
        self.base_page.auth(username, password)
        locator = getattr(self.home_page.locators, LOCATORS[0])
        hover_element = self.base_page.find(getattr(self.home_page.locators, LOCATORS[2]))
        hover = ActionChains(self.driver).move_to_element(hover_element)
        hover.perform()
        self.home_page.click(locator)
        if len(self.driver.window_handles) == 2:
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
        assert LOCATORS[1] in self.driver.page_source
