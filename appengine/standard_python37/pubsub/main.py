# Copyright 2019 Google, LLC.
#
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

# [START app]
import base64
from flask import current_app, Flask, render_template, request
import json
import logging
import os

from google.auth import jwt
from google.auth.transport import requests
from google.cloud import pubsub_v1
from google.oauth2 import id_token


app = Flask(__name__)

# Configure the following environment variables via app.yaml
# This is used in the push request handler to verify that the request came from
# pubsub and originated from a trusted source.
app.config['PUBSUB_VERIFICATION_TOKEN'] = \
    os.environ['PUBSUB_VERIFICATION_TOKEN']
app.config['PUBSUB_TOPIC'] = os.environ['PUBSUB_TOPIC']
app.config['GCLOUD_PROJECT'] = os.environ['GOOGLE_CLOUD_PROJECT']

# Global list to store messages, tokens, etc. received by this instance.
MESSAGES = []
TOKENS = []
HEADERS = []
CLAIMS = []

# [START index]
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', messages=MESSAGES, tokens=TOKENS,
                               headers=HEADERS, claims=CLAIMS)

    data = request.form.get('payload', 'Example payload').encode('utf-8')

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(app.config['GCLOUD_PROJECT'],
                                      app.config['PUBSUB_TOPIC'])
    future = publisher.publish(topic_path, data)
    future.result()
    return 'OK', 200
# [END index]


# [START push]
@app.route('/_ah/push-handlers/receive_messages', methods=['POST'])
def receive_messages_handler():
    # Verify that the request originates from the application.
    if (request.args.get('token', '') !=
            current_app.config['PUBSUB_VERIFICATION_TOKEN']):
        return 'Invalid request', 400

    # Verify that the push request originates from Cloud Pub/Sub.
    try:
        # Get the Cloud Pub/Sub-generated JWT in the "Authorization" header.
        bearer_token = request.headers.get('Authorization')
        token = bearer_token.split(' ')[1]
        TOKENS.append(token)

        header = jwt.decode_header(token)
        HEADERS.append(header)

        # Verify and decode the JWT. Underneath it checks the signature against
        # Google's public certs at https://www.googleapis.com/oauth2/v1/certs.
        # It also checks the token expiration time.
        claim = id_token.verify_oauth2_token(token, requests.Request())
        CLAIMS.append(claim)

        # Check the audience field in the claim. It was specified in
        # `--push-auth-token-audience` when you created the subscription.
        assert claim['aud'] == 'example.com'
    except Exception as e:
        return 'Invalid token: {}\n'.format(e), 400

    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])
    MESSAGES.append(payload)
    # Returning any 2xx status indicates successful receipt of the message.
    return 'OK', 200
# [END push]


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
