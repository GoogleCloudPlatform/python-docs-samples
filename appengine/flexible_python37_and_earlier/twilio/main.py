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

import logging
import os

from flask import Flask, request
from twilio import rest
from twilio.twiml import messaging_response, voice_response


TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER = os.environ['TWILIO_NUMBER']


app = Flask(__name__)


# [START gae_flex_twilio_receive_call]
@app.route('/call/receive', methods=['POST'])
def receive_call():
    """Answers a call and replies with a simple greeting."""
    response = voice_response.VoiceResponse()
    response.say('Hello from Twilio!')
    return str(response), 200, {'Content-Type': 'application/xml'}
# [END gae_flex_twilio_receive_call]


# [START gae_flex_twilio_send_sms]
@app.route('/sms/send')
def send_sms():
    """Sends a simple SMS message."""
    to = request.args.get('to')
    if not to:
        return ('Please provide the number to message in the "to" query string'
                ' parameter.'), 400

    client = rest.Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    rv = client.messages.create(
        to=to,
        from_=TWILIO_NUMBER,
        body='Hello from Twilio!'
    )
    return str(rv)
# [END gae_flex_twilio_send_sms]


# [START gae_flex_twilio_receive_sms]
@app.route('/sms/receive', methods=['POST'])
def receive_sms():
    """Receives an SMS message and replies with a simple greeting."""
    sender = request.values.get('From')
    body = request.values.get('Body')

    message = 'Hello, {}, you said: {}'.format(sender, body)

    response = messaging_response.MessagingResponse()
    response.message(message)
    return str(response), 200, {'Content-Type': 'application/xml'}
# [END gae_flex_twilio_receive_sms]


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
