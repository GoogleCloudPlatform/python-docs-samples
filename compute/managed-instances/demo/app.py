#!/usr/bin/python3
from flask import Flask, make_response, render_template
from re import sub
from requests import get
from socket import gethostname

PORT_NUMBER = 80

app = Flask(__name__)
is_healthy = True


@app.route('/')
def index():
    return render_template('index.html',
                           hostname=_get_hostname(),
                           zone=_get_zone(),
                           template=_get_template(),
                           healthy=is_healthy)


@app.route('/health')
def health():
    global is_healthy
    status = 200 if is_healthy else 500
    return make_response(render_template('health.html', healthy=healthy), status)


@app.route('/makeHealthy')
def make_healthy():
    global is_healthy
    is_healthy = True
    response = make_response(render_template('index.html',
                                             hostname=gethostname(),
                                             zone=_get_zone(),
                                             template=_get_template(),
                                             healthy=True), 302)
    response.headers['Location'] = '/'
    return response


@app.route('/makeUnhealthy')
def make_unhealthy():
    global is_healthy
    is_healthy = False
    response = make_response(render_template('index.html',
                                             hostname=gethostname(),
                                             zone=_get_zone(),
                                             template=_get_template(),
                                             healthy=False), 302)
    response.headers['Location'] = '/'
    return response


def _get_zone():
    r = get('http://metadata.google.internal/'
            'computeMetadata/v1/instance/zone',
            headers={'Metadata-Flavor': 'Google'})
    if r.status_code == 200:
        return sub(r'.+zones/(.+)', r'\1', r.text)
    else:
        return ''


def _get_template():
    r = get('http://metadata.google.internal/'
            'computeMetadata/v1/instance/attributes/instance-template',
            headers={'Metadata-Flavor': 'Google'})
    if r.status_code == 200:
        return sub(r'.+instanceTemplates/(.+)', r'\1', r.text)
    else:
        return ''


if __name__ == "__main__":
    app.run(debug=False, port=80)
