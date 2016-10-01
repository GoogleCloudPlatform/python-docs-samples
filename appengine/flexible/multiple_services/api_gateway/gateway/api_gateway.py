import requests
import sys
import os
from flask import Flask
app = Flask(__name__)

#development ports {static: 8003, flask1: 8001, flask2: 8002}
@app.route('/environment')
def get_env():
    return str(os.environ)

@app.route('/test')
def test():
    return "GATEWAY OPERATIONAL"

@app.route('/')
def root():
    print(os.environ)
    print(os.environ['GAE_LONG_APP_ID'])
    print('https://static-dot-' + os.environ['GAE_LONG_APP_ID'] + '.appspot.com')
    # return 'https://static-dot-' + os.environ['GAE_LONG_APP_ID'] + '.appspot.com'
    res = requests.get('https://static-dot-' + os.environ['GAE_LONG_APP_ID'] + '.appspot.com')
    return res.content

@app.route('/hello/<service>')
def say_hello(service):
    services = {
        'flask1': { 'url': 'https://flask1-dot-' + os.environ['GAE_LONG_APP_ID'] + '.appspot.com', 'send': False },
        'flask2': { 'url': 'https://flask2-dot-' + os.environ['GAE_LONG_APP_ID'] + '.appspot.com', 'send': False }
    }
    if service == 'everyone':
        for key, val in services.items():
            val['send'] = True
    else:
        services[service]['send'] = True

    responses = []
    for key, val in services.items():
        if val['send'] == True:
            res = requests.get(val['url'] + '/hello')
            responses.append(res.content)

    return '\n'.encode().join(responses)

@app.route('/<path>')
def static_file(path):
    res = requests.get('https://static-dot-' + os.environ['GAE_LONG_APP_ID'] + '.appspot.com' + '/' + path)
    return res.content, 200, {'Content-Type': res.headers['Content-Type']}


if __name__  == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'development':
        app.run(port=int(8000))
    else:
        app.run()
