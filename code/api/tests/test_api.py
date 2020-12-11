import pytest
from functions.rand_user import create_user
from api.client.api_client import ApiClient
from database.builder.mysql_orm_builder import MySqlOrmBuilder
from database.client.mysql_orm_client import SQLOrmClient

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

    @pytest.mark.API
    def test_add_user(self):
        """
            Тестируется добавление валидного пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на добавление валидного пользователя.
            В ответе ожидается сообщение и статус-код 201.
        """
        username, email, password = create_user()
        assert self.api_client.add_user(username, password, email).status_code == 201

    @pytest.mark.API
    def test_add_exist_user(self, user):
        """
            Тестируется добавление существующего валидного пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на добавление валидного пользователя.
            В ответе ожидается сообщение и статус-код 304.
        """
        username, email, password = user
        assert self.api_client.add_user(username, password, email).status_code == 304

    @pytest.mark.API
    def test_del_exist_user(self):
        """
            Тестируется удаления пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Через базу данных добавляется пользователь.
            3. Отправляется запрос на удаления существующего валидного пользователя.
            В ответе ожидается сообщение и статус-код 204.
        """
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 1, 0)
        assert self.api_client.delete_user(username).status_code == 204

    @pytest.mark.API
    def test_del_nonexistent_user(self):
        """
            Тестируется удаления несуществующего пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на удаления несуществующего валидного пользователя.
            В ответе ожидается сообщение и статус-код 404.
        """
        assert self.api_client.delete_user('dasdjq').status_code == 404

    @pytest.mark.API
    def test_block_user(self):
        """
            Тестируется блокировка пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Через базу данных добавляется пользователь.
            3. Отправляется запрос на блокировку существуещего валидного пользователя.
            В ответе ожидается сообщение и статус-код 200.
        """
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 1, 0)
        assert self.api_client.block_user(username).status_code == 200

    @pytest.mark.API
    def test_negative_block_user(self):
        """
            Тестируется блокировка заблокированного пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Через базу данных добавляется заблокированный пользователь.
            3. Отправляется запрос на блокировку существуещего заблокированного валидного пользователя.
            В ответе ожидается сообщение и статус-код 304.
        """
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 0, 0)
        assert self.api_client.block_user(username).status_code == 304

    @pytest.mark.API
    def test_block_nonexistent_user(self):
        """
            Тестируется блокировка несуществуещего пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на блокировку несуществуещего валидного пользователя.
            В ответе ожидается сообщение и статус-код 404.
        """
        assert self.api_client.block_user('fhsiusdf').status_code == 404

    @pytest.mark.API
    def test_unblock_user(self):
        """
            Тестируется разблокировка пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Через базу данных добавляется заблокированный пользователь.
            3. Отправляется запрос на разблокировку валидного пользователя.
            В ответе ожидается сообщение и статус-код 200.
        """
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 0, 0)
        assert self.api_client.unblock_user(username).status_code == 200

    @pytest.mark.API
    def test_unblock_nonexistent_user(self):
        """
            Тестируется разблокировка несуществуещего пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Отправляется запрос на разблокировку несуществуещего пользователя.
            В ответе ожидается сообщение и статус-код 404.
        """
        assert self.api_client.unblock_user('fsdfjdas').status_code == 404

    @pytest.mark.API
    def test_negative_unblock_user(self):
        """
            Тестируется разблокировка незаблокированного пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Через базу данных добавляется пользователь.
            3. Отправляется запрос на разблокировку валидного пользователя.
            В ответе ожидается сообщение и статус-код 304.
        """
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 1, 0)
        assert self.api_client.unblock_user(username).status_code == 304

    @pytest.mark.API
    def test_auth_via_blocked_user(self, blocked_user):
        """
            Тестируется авторизация через заблокированного пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Через базу данных добавляется заблокированный пользователь.
            3. Отправляется запрос на авторизацию через заблокированного пользователя.
            В ответе ожидается сообщение и статус-код 401.
        """
        username, email, password = blocked_user
        self.api_client.logout()
        assert self.api_client.auth(username, password).status_code == 401