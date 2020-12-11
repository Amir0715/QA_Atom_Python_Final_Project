from selenium.webdriver.common.by import By


class HomePageLocators(object):

    HOME_MENU_LOCATOR = (By.XPATH, '//*[@id="wrap"]/header/nav/ul/li[1]/a')
    PYTHON_MENU_LOCATOR = (By.XPATH, '//*[@id="wrap"]/header/nav/ul/li[2]/a')
    PYTHON_FLASK_MENU_LOCATOR = (By.XPATH, '//*[@id="wrap"]/header/nav/ul/li[2]/div/ul/li[2]/a')
    PYTHON_HISTORY_MENU_LOCATOR = (By.XPATH, '//*[@id="wrap"]/header/nav/ul/li[2]/div/ul/li[1]/a')
    LINUX_MENU_LOCATOR = (By.XPATH, '//*[@id="wrap"]/header/nav/ul/li[3]')
    LINUX_FEDORA_MENU_LOCATOR = (By.XPATH, '//*[@id="wrap"]/header/nav/ul/li[3]/div/ul/li/a')
    NETWORK_MENU_LOCATOR = (By.XPATH, '//*[@id="wrap"]/header/nav/ul/li[4]')
    NETWORK_WIRESHARK_NEWS_MENU_LOCATOR = (By.XPATH, '//*[@id="wrap"]/header/nav/ul/li[4]/div/ul/li[1]/ul/li[1]/a')
    NETWORK_WIRESHARK_DOWNLOAD_MENU_LOCATOR = (By.XPATH, '//*[@id="wrap"]/header/nav/ul/li[4]/div/ul/li[1]/ul/li[2]/a')
    NETWORK_TCPDUMP_MENU_LOCATOR = (By.XPATH, '//*[@id="wrap"]/header/nav/ul/li[4]/div/ul/li[2]/ul/li/a')

    API_HREF_LOCATOR = (By.XPATH, '//*[@id="content"]/div[2]/div[1]/figure/a')
    INTERNET_HREF_LOCATOR = (By.XPATH, '//*[@id="content"]/div[2]/div[2]/figure/a')
    SMTP_HREF_LOCATOR = (By.XPATH, '//*[@id="content"]/div[2]/div[3]/figure/a')

    LOGOUT_BUTTON_LOCATOR = (By.XPATH, '//*[@id="logout"]/a')

