# Copyright 2015 Google Inc. All Rights Reserved.
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
import requests

# [START config]
MAILGUN_DOMAIN_NAME = os.environ['MAILGUN_DOMAIN_NAME']
MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']
# [END config]

app = Flask(__name__)


# [START simple_message]
def send_simple_message(to):
    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
    auth = ('api', MAILGUN_API_KEY)
    data = {
        'from': 'Mailgun User <mailgun@{}>'.format(MAILGUN_DOMAIN_NAME),
        'to': to,
        'subject': 'Simple Mailgun Example',
        'text': 'Plaintext content',
    }

    response = requests.post(url, auth=auth, data=data)
    response.raise_for_status()
# [END simple_message]


# [START complex_message]
def send_complex_message(to):
    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
    auth = ('api', MAILGUN_API_KEY)
    data = {
        'from': 'Mailgun User <mailgun@{}>'.format(MAILGUN_DOMAIN_NAME),
        'to': to,
        'subject': 'Complex Mailgun Example',
        'text': 'Plaintext content',
        'html': '<html>HTML <strong>content</strong></html>'
    }
    files = [("attachment", open("example-attachment.txt"))]

    response = requests.post(url, auth=auth, data=data, files=files)
    response.raise_for_status()
# [END complex_message]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send/email', methods=['POST'])
def send_email():
    action = request.form.get('submit')
    to = request.form.get('to')

    if action == 'Send simple email':
        send_simple_message(to)
    else:
        send_complex_message(to)

    return 'Email sent.'


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
