# Copyright 2019, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, make_response, render_template
from re import sub
from requests import get
from socket import gethostname

PORT_NUMBER = 80

app = Flask(__name__)
healthy = True


@app.route('/')
def index():
    global healthy
    return render_template('index.html',
                           hostname=_get_hostname(),
                           zone=_get_zone(),
                           template=_get_template(),
                           healthy=healthy)


@app.route('/health')
def health():
    global healthy
    status = 200 if healthy else 500
    return make_response(render_template('health.html', healthy=healthy), status)


@app.route('/makeHealthy')
def make_healthy():
    global healthy
    healthy = True
    response = make_response(render_template('index.html',
                                             hostname=gethostname(),
                                             zone=_get_zone(),
                                             template=_get_template(),
                                             healthy=True), 302)
    response.headers['Location'] = '/'
    return response


@app.route('/makeUnhealthy')
def make_unhealthy():
    global healthy
    healthy = False
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
