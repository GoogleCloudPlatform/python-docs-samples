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
import sendgrid
from sendgrid.helpers import mail

# [START config]
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
SENDGRID_SENDER = os.environ['SENDGRID_SENDER']
# [END config]

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# [START example]
@app.route('/send/email', methods=['POST'])
def send_email():
    to = request.form.get('to')
    if not to:
        return ('Please provide an email address in the "to" query string '
                'parameter.'), 400

    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

    to_email = mail.Email(to)
    from_email = mail.Email(SENDGRID_SENDER)
    subject = 'This is a test email'
    content = mail.Content('text/plain', 'Example message.')
    message = mail.Mail(from_email, subject, to_email, content)

    response = sg.client.mail.send.post(request_body=message.get())

    if response.status_code != 202:
        return 'An error occurred: {}'.format(response.body), 500

    return 'Email sent.'
# [END example]


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
