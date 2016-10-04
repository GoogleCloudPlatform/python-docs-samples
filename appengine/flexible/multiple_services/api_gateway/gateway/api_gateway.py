import requests
import sys
import os
from flask import Flask
app = Flask(__name__)

@app.route('/environment')
def get_env():
    configuration = 'production'
    return app.config['MODE']

@app.route('/test')
def test():
    return "GATEWAY OPERATIONAL"

@app.route('/')
def root():
    urls = {
        'development': 'http://localhost:8003',
        'production': 'https://static-dot-' + os.environ.get('GAE_LONG_APP_ID', '') + '.appspot.com'
    }
    environment = app.config['MODE']
    print(environment)
    print(urls[environment])
    res = requests.get(urls[environment])
    return res.content

@app.route('/hello/<service>')
def say_hello(service):
    environment = app.config['MODE']
    services = {
        'production': {
            'flask1': { 'url': 'https://flask1-dot-' + os.environ.get('GAE_LONG_APP_ID', '') + '.appspot.com', 'send': False },
            'flask2': { 'url': 'https://flask2-dot-' + os.environ.get('GAE_LONG_APP_ID', '') + '.appspot.com', 'send': False }
        },
        'development': {
            'flask1': {'url': 'http://localhost:8001', 'send': False },
            'flask2': {'url': 'http://localhost:8002', 'send': False }
        }
    }
    environment = app.config['MODE']
    if service == 'everyone':
        for key, val in services[environment].items():
            val['send'] = True
    else:
        services[environment][service]['send'] = True

    responses = []
    for key, val in services[environment].items():
        if val['send'] == True:
            res = requests.get(val['url'] + '/hello')
            responses.append(res.content)

    return '\n'.encode().join(responses)

@app.route('/<path>')
def static_file(path):
    environment = app.config['MODE']
    url = {
        'development': 'http://localhost:8003',
        'production': 'https://static-dot-' + os.environ.get('GAE_LONG_APP_ID', '') + '.appspot.com'
    }
    res = requests.get(url[environment] + '/' + path)
    return res.content, 200, {'Content-Type': res.headers['Content-Type']}


if __name__  == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--development':
        app.config['MODE'] = 'development'
        app.config['DEBUG'] = True
        app.run(port=int(8000))
    else:
        app.config['MODE'] = 'production'
        app.run()
