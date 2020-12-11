import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

# Первый запуск:
# Создать бд
# Создать таблицу
# Создать пользователей

# def pytest_configure(config):
#     if not hasattr(config, 'slaveinput'):
#         try:
#             subprocess.call(['docker-compose', 'up'], timeout=35, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         except subprocess.TimeoutExpired:
#             subprocess.call(['docker', 'ps'])
#
#     config.connection = MySQLConnector(
#         hostname='127.0.0.1',
#         port='3306',
#         username='root',
#         password='root',
#         db='users'
#     )
#     if not hasattr(config, 'slaveinput'):
#         config.connection.connect_master()
#
#         config.connection.add_user(User(
#             username='ikramanop',
#             password='1234567890',
#             email='asertolpas@gmail.com',
#             access=1,
#             active=0
#         ))
#
#         config.connection.add_user(User(
#             username='zvozsky',
#             password='1234567890',
#             email='afjefnjsebnf@fsiejf.er',
#             access=1,
#             active=0
#         ))
#
#         config.connection.add_user(User(
#             username='k12f2432',
#             password='1234567890',
#             email='njsebnf@fsif.er',
#             access=1,
#             active=0
#         ))
#     else:
#         config.connection.connect_slave()


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    selenoid = request.config.getoption('--selenoid_host')
    return {'url': url, 'selenoid_host': selenoid}


def pytest_addoption(parser):
    parser.addoption('--url', default='http://127.0.0.1:8080')
    parser.addoption('--selenoid_host', default=None)


@pytest.fixture(scope='function')
def driver(config):
    driver = None

    if config['selenoid_host'] is not None:
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "86.0",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False
            }
        }
        selenoid_url = 'http://' + config['selenoid_host'] + '/wd/hub'
        options = ChromeOptions()
        driver = webdriver.Remote(command_executor=selenoid_url, options=options, desired_capabilities=capabilities)
    else:
        options = ChromeOptions()
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options,
                                  desired_capabilities=DesiredCapabilities().CHROME)
    driver.maximize_window()
    driver.get(config['url'])
    yield driver
    driver.quit()
