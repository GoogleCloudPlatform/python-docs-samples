# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
import requests

import services_config

app = Flask(__name__)
services_config.init_app(app)


@app.route('/')
def root():
    """Gets index.html from the static file server"""
    res = requests.get(app.config['SERVICE_MAP']['static'])
    return res.content


@app.route('/hello/<service>')
def say_hello(service):
    """Recieves requests from buttons on the front end and resopnds
    or sends request to the static file server"""
    # If 'gateway' is specified return immediate
    if service == 'gateway':
        return 'Gateway says hello'

    # Otherwise send request to service indicated by URL param
    responses = []
    url = app.config['SERVICE_MAP'][service]
    res = requests.get(url + '/hello')
    responses.append(res.content)
    return '\n'.encode().join(responses)


@app.route('/<path>')
def static_file(path):
    """Gets static files required by index.html to static file server"""
    url = app.config['SERVICE_MAP']['static']
    res = requests.get(url + '/' + path)
    return res.content, 200, {'Content-Type': res.headers['Content-Type']}


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8000, debug=True)
