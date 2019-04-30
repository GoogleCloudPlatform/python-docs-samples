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
"""
Flask app to be used as an interactive demonstration of autohealing.

Exposes a simple UI showing basic server stats and a toggle button to
simulate a healthy/unhealthy server status for any attached health check.

Attached health checks should query the '/health' path.
"""

from flask import Flask, make_response, render_template
from re import sub
from requests import get
from socket import gethostname

PORT_NUMBER = 80

app = Flask(__name__)
healthy = True


@app.route('/')
def index():
    """Returns the demo UI."""
    global healthy
    return render_template('index.html',
                           hostname=gethostname(),
                           zone=_get_zone(),
                           template=_get_template(),
                           healthy=healthy)


@app.route('/health')
def health():
    """Returns the simulated 'healthy'/'unhealthy' status of the server.

    Returns:
        HTTP status 200 if 'healthy', HTTP status 500 if 'unhealthy'
    """
    global healthy
    template = render_template('health.html', healthy=healthy)
    return make_response(template, 200 if healthy else 500)


@app.route('/makeHealthy')
def make_healthy():
    """Sets the server to simulate a 'healthy' status."""
    global healthy
    healthy = True
    template = render_template('index.html',
                               hostname=gethostname(),
                               zone=_get_zone(),
                               template=_get_template(),
                               healthy=True)
    response = make_response(template, 302)
    response.headers['Location'] = '/'
    return response


@app.route('/makeUnhealthy')
def make_unhealthy():
    """Sets the server to simulate an 'unhealthy' status."""
    global healthy
    healthy = False
    template = render_template('index.html',
                               hostname=gethostname(),
                               zone=_get_zone(),
                               template=_get_template(),
                               healthy=False)
    response = make_response(template, 302)
    response.headers['Location'] = '/'
    return response


def _get_zone():
    """Gets the GCE zone of this instance.

    Returns:
        str: The name of the zone if the zone was successfully determined.
        Empty string otherwise.
    """
    r = get('http://metadata.google.internal/'
            'computeMetadata/v1/instance/zone',
            headers={'Metadata-Flavor': 'Google'})
    if r.status_code == 200:
        return sub(r'.+zones/(.+)', r'\1', r.text)
    else:
        return ''


def _get_template():
    """Gets the GCE instance template of this instance.

    Returns:
        str: The name of the template if the template was successfully
        determined and this instance was built using an instance template.
        Empty string otherwise.
    """
    r = get('http://metadata.google.internal/'
            'computeMetadata/v1/instance/attributes/instance-template',
            headers={'Metadata-Flavor': 'Google'})
    if r.status_code == 200:
        return sub(r'.+instanceTemplates/(.+)', r'\1', r.text)
    else:
        return ''


if __name__ == "__main__":
    app.run(debug=False, port=PORT_NUMBER)
