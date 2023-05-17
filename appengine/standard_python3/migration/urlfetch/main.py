# Copyright 2020 Google LLC
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

from flask import Flask, render_template, request
from google.auth.transport import requests as reqs
from google.oauth2 import id_token
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def make_request():
    url = request.form['url']
    token = id_token.fetch_id_token(reqs.Request(), url)

    resp = requests.get(
        url,
        headers={'Authorization': f'Bearer {token}'}
    )

    message = f'Response when calling {url}:\n\n'
    message += resp.text

    return message, 200, {'Content-type': 'text/plain'}
