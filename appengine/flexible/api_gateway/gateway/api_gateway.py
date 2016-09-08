import requests
import sys
from flask import Flask
app = Flask(__name__)

@app.route('/test')
def test():
    return "GATEWAY OPERATIONAL"

@app.route('/')
def root():
    res = requests.get('https://template-dot-flask-algo.appspot.com/')
    return res.content

@app.route('/hello/<service>')
def say_hello(service):

    services = {
        'flask': { 'url': 'https://flask-dot-flask-algo.appspot.com/', 'send': False },
        'express': {'url': 'https://express-dot-flask-algo.appspot.com/', 'send': False }
    }

    if service == 'everyone':
        for key, val in services.items():
            val['send'] = True
    else:
        services[service]['send'] = True

    responses = []
    for key, val in services.items():
        if val['send'] == True:
            res = requests.get(val['url'] + 'hello')
            responses.append(res.content)

    return '\n'.encode().join(responses)

@app.route('/<path>')
def static_file(path):
    res = requests.get('https://template-dot-flask-algo.appspot.com/' + path)
    return res.content, 200, {'Content-Type': res.headers['Content-Type']}


if __name__  == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'development':
        app.run(port=int(5000))
    else:
        app.run()
