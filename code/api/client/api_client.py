import json
from urllib.parse import urljoin
import requests


class ApiClient:
    GET = "GET"
    POST = "POST"

    def __init__(self, host, port):
        self.session = requests.Session()
        self.host = host
        self.port = port
        self.url = "http://" + self.host + ":" + str(self.port)
        self.cookies = None

    def auth(self, username, password):
        location = "/login"
        content_type = "application/x-www-form-urlencoded"
        connection = "keep-alive"
        headers = {
            'Content-Type': content_type,
            'Connection': connection
        }
        body = {
            'username': username,
            'password': password,
            'submit': 'Login'
        }
        response = self._request(method=self.POST, location=location, headers=headers, data=body)
        self.cookies = response.headers['Set-Cookie'].split(';')[0]
        return response

    def add_user(self, username, password, email):
        location = "/api/add_user"
        content_type = "application/json"

        headers = {
            'Content-Type': content_type,
            'Cookie': self.cookies
        }

        body = {
            'username': username,
            'password': password,
            'email': email
        }
        body = json.dumps(body)

        return self._request(method=self.POST, location=location, headers=headers, data=body)

    def delete_user(self, username):
        location = "/api/del_user/" + username

        return self._request(method=self.GET, location=location)

    def block_user(self, username):
        location = "/api/block_user/" + username

        return self._request(method=self.GET, location=location)

    def unblock_user(self, username):
        location = "/api/accept_user/" + username

        return self._request(method=self.GET, location=location)

    def status(self):
        location = "/status"

        return self._request(method=self.GET, location=location)

    def logout(self):
        location = "/logout"

        return self._request(method=self.GET, location=location)

    def _request(self, method, url=None, location=None, headers=None, params=None, data=None, json=False,
                 allow_redirects=False):
        """
        Обертка для метода request, нужен для взаимодействия с апи через объект сессию
        """
        if location is not None and url is None:
            url = urljoin(self.url, location)

        res = self.session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            allow_redirects=allow_redirects
        )
        if json:
            return res.json()
        else:
            return res


if __name__ == '__main__':
    api = ApiClient(host='127.0.0.1', port=8080)
    print(api.auth(*('amir0715', '123456')))
    print(api.block_user('amir1234'))
    print(api.unblock_user('amir1234'))
    print(api.status())
    print(api.add_user('kamolov2', '123456', 'kamolov2@mail.ru'))
    print(api.delete_user('kamolov2'))
