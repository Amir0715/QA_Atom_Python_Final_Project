from functions.rand_user import create_user
from ui.tests.base import BaseCase
from ui.fixtures.pageObject_fixtures import *

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

    @pytest.mark.UI_DB
    def test_reg(self):
        """
            Тестируется регистрация пользователя через UI и проверка записи в базе данных.
            Шаги:
            1. Происходит регистрация через форму.
            Ожидается что регистрация пройдет и в базе данных появится запись.
        """
        username, email, password = create_user()
        self.base_page.go_to_reg()
        self.reg_page.reg(username, email, password)
        assert self.MySqlBuilder.get_user(username) is not None
        self.MySqlBuilder.del_user(username)

    @pytest.mark.UI_DB
    def test_negative_reg(self):
        """
            Тестируется регистрация существуещего пользователя через UI и проверка записи в базе данных.
            Шаги:
            1. Происходит регистрация через форму.
            1. Происходит регистрация через форму.
            Ожидается что запись будет добавлена один раз в базу данных.
        """
        username, email, password = create_user()
        self.base_page.go_to_reg()
        self.reg_page.reg(username, email, password)
        self.home_page.click(self.home_page.locators.LOGOUT_BUTTON_LOCATOR)
        self.base_page.go_to_reg()
        self.reg_page.reg(username, email, password)
        assert self.MySqlBuilder.get_user(username) is not None