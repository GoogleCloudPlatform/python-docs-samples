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

# [START app]
import logging

from flask import Flask, make_response

# [START imports]
from requests_futures.sessions import FuturesSession
from time import sleep
# [END imports]


TIMEOUT = 10    # Wait this many seconds for background calls to finish
app = Flask(__name__)


@app.route('/')     # Fetch and return remote page asynchronously
def get_async():
    # [START requests_get]
    session = FuturesSession()
    url = 'http://www.google.com/humans.txt'

    rpc = session.get(url)

    # ... do other things ...

    resp = make_response(rpc.result().text)
    resp.headers['Content-type'] = 'text/plain'
    return resp
    # [END requests_get]


@app.route('/callback')     # Fetch and return remote pages using callback
def get_callback():
    global response_text
    global counter

    response_text = ''
    counter = 0

    def cb(resp, *args, **kwargs):
        global response_text
        global counter

        if 300 <= resp.status_code < 400:
            return  # ignore intermediate redirection responses

        counter += 1
        response_text += 'Response number {} is {} bytes from {}\n'.format(
            counter, len(resp.text), resp.url)

    session = FuturesSession()
    urls = [
        'https://google.com/',
        'https://www.google.com/humans.txt',
        'https://www.github.com',
        'https://www.travis-ci.org'
    ]

    futures = [session.get(url, hooks={'response': cb}) for url in urls]

    # No wait functionality in requests_futures, so check every second to
    # see if all callbacks are done, up to TIMEOUT seconds
    for elapsed_time in range(TIMEOUT+1):
        all_done = True
        for future in futures:
            if not future.done():
                all_done = False
                break
        if all_done:
            break
        sleep(1)

    resp = make_response(response_text)
    resp.headers['Content-type'] = 'text/plain'
    return resp


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
# [END app]
