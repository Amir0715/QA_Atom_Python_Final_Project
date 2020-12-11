from flask import Flask, request, json, make_response
import threading

app = Flask(__name__)

valid_users = {'vk_mock_id_qa' : '1234'}

def run_mock(host, port):
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    terminate = request.environ.get('werkzeug.server.shutdown')
    if terminate:
        terminate()


@app.route('/vk_id/<username>', methods=['GET'])
def get_user(username):
    user = valid_users.get(username, None)
    result = {}
    if user:
        result = {'vk_id': user}
        res = make_response(result)
        res.headers['Status'] = '200 OK'
        res.headers['Content-Type'] = 'application/json'
        res.headers['Response'] = result
        return res
    else:
        res = make_response(result)
        res.headers['Status'] = '400 Not Found'
        res.headers['Content-Type'] = 'application/json'
        res.headers['Response'] = result
        return res


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_mock()
    return 'Shutting down...'

@app.route('/api_id/add', methods=['POST'])
def add_valid_user():
    pass

if __name__ == '__main__':
    run_mock(host='0.0.0.0', port=5000)