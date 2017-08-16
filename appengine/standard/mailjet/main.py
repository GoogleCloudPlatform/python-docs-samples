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

# [START app]
import logging
import os

from flask import Flask, render_template, request
# [START config]
import mailjet_rest
import requests_toolbelt.adapters.appengine

# Use the App Engine requests adapter to allow the requests library to be
# used on App Engine.
requests_toolbelt.adapters.appengine.monkeypatch()

MAILJET_API_KEY = os.environ['MAILJET_API_KEY']
MAILJET_API_SECRET = os.environ['MAILJET_API_SECRET']
MAILJET_SENDER = os.environ['MAILJET_SENDER']
# [END config]

app = Flask(__name__)


# [START send_message]
def send_message(to):
    client = mailjet_rest.Client(
        auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')

    data = {
        'Messages': [{
            "From": {
                "Email": MAILJET_SENDER,
                "Name": 'App Engine Standard Mailjet Sample'
            },
            "To": [{
                "Email": to
            }],
            "Subject": 'Example email.',
            "TextPart": 'This is an example email.',
            "HTMLPart": 'This is an <i>example</i> email.'
        }]
    }

    result = client.send.create(data=data)

    return result.json()
# [END send_message]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send/email', methods=['POST'])
def send_email():
    to = request.form.get('to')

    result = send_message(to)

    return 'Email sent, response: <pre>{}</pre>'.format(result)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
# [END app]
