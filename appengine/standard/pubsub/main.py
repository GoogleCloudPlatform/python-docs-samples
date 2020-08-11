# Copyright 2018 Google, LLC.
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
import json
import logging
import os

from flask import current_app, Flask, render_template, request
from googleapiclient.discovery import build


app = Flask(__name__)

# Configure the following environment variables via app.yaml
# This is used in the push request handler to verify that the request came from
# pubsub and originated from a trusted source.
app.config['PUBSUB_VERIFICATION_TOKEN'] = \
    os.environ['PUBSUB_VERIFICATION_TOKEN']
app.config['PUBSUB_TOPIC'] = os.environ['PUBSUB_TOPIC']
app.config['GOOGLE_CLOUD_PROJECT'] = os.environ['GOOGLE_CLOUD_PROJECT']


# Global list to storage messages received by this instance.
MESSAGES = []


# [START index]
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', messages=MESSAGES)

    data = request.form.get('payload', 'Example payload').encode('utf-8')

    service = build('pubsub', 'v1')
    topic_path = 'projects/{project_id}/topics/{topic}'.format(
        project_id=app.config['GOOGLE_CLOUD_PROJECT'],
        topic=app.config['PUBSUB_TOPIC']
    )
    service.projects().topics().publish(
        topic=topic_path, body={
          "messages": [{
              "data": base64.b64encode(data)
          }]
        }).execute()

    return 'OK', 200
# [END index]


# [START push]
@app.route('/_ah/push-handlers/receive_messages', methods=['POST'])
def receive_messages_handler():
    if (request.args.get('token', '') !=
            current_app.config['PUBSUB_VERIFICATION_TOKEN']):
        return 'Invalid request', 400

    envelope = json.loads(request.get_data().decode('utf-8'))
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
