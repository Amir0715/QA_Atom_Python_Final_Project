import pytest
from api.client.api_client import ApiClient
from database.builder.mysql_orm_builder import MySqlOrmBuilder
from database.client.mysql_orm_client import SQLOrmClient
from functions.rand_user import create_user


class TestApi:

    @pytest.fixture(scope='function', autouse=True)
    def client(self):
        self.api_client = ApiClient(host='127.0.0.1', port=8080)
        self.MySqlClient = SQLOrmClient(user='test_qa', password="qa_test", host='127.0.0.1', port=3306, db_name='test')
        self.MySqlBuilder = MySqlOrmBuilder(self.MySqlClient)
        username, password, email = create_user()
        self.MySqlBuilder.add_user(username=username, email=email, password=password, access=1, active=0)
        self.api_client.auth(username, password)
        yield self.api_client
        self.MySqlBuilder.del_user(username)

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

    @pytest.mark.API_DB
    def test_add_user(self):
        """
            Тестируется добавление валидного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на добавление валидного пользователя.
            Ожидается появления записи в базе данных.
        """
        username, email, password = create_user()
        self.api_client.add_user(username, password, email)
        assert self.MySqlBuilder.get_user(username) is not None

    @pytest.mark.API_DB
    def test_add_exist_user(self, user):
        """
            Тестируется добавление существующего валидного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на добавление валидного пользователя.
            Ожидается существования записи в базе данных.
        """
        username, email, password = user
        self.api_client.add_user(username, password, email)
        assert self.MySqlBuilder.get_user(username) is not None

    @pytest.mark.API_DB
    def test_del_exist_user(self):
        """
            Тестируется удаления существующего валидного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на удаления валидного пользователя.
            Ожидается удаления записи в базе данных.
        """
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 1, 0)
        self.api_client.delete_user(username)
        assert self.MySqlBuilder.get_user(username) is None

    @pytest.mark.API_DB
    def test_del_nonexistent_user(self):
        """
            Тестируется удаления несуществующего пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на удаления несуществующего пользователя.
            Ожидается неизменость базы данных.
        """
        username = 'dasdjq'
        self.api_client.delete_user(username)
        assert self.MySqlBuilder.get_user(username) is None

    @pytest.mark.API_DB
    def test_block_user(self):
        """
            Тестируется блокировка валидного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на блокировку существующего пользователя.
            Ожидается что поле доступа изменится на 0 в базе данных.
        """
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 1, 0)
        self.api_client.block_user(username)
        assert self.MySqlBuilder.get_user(username).access == 0

    @pytest.mark.API_DB
    def test_negative_block_user(self):
        """
            Тестируется блокировка заблокированного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на блокировку заблокированного существующего пользователя.
            Ожидается что поле доступа неизменится в базе данных.
        """
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 0, 0)
        self.api_client.block_user(username)
        assert self.MySqlBuilder.get_user(username).access == 0

    @pytest.mark.API_DB
    def test_unblock_user(self):
        """
            Тестируется разблокировка валидного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на разблокировку существующего пользователя.
            Ожидается что поле доступа изменится на 1 в базе данных.
        """
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 0, 0)
        self.api_client.unblock_user(username)
        assert self.MySqlBuilder.get_user(username).access == 1

    @pytest.mark.API_DB
    def test_negative_unblock_user(self):
        """
            Тестируется разблокировка незаблокированного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на разблокировку не заблокированного существующего пользователя.
            Ожидается что поле доступа неизменится в базе данных.
        """
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 1, 0)
        self.api_client.unblock_user(username)
        assert self.MySqlBuilder.get_user(username).access == 1