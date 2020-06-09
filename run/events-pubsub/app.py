# Copyright 2020 Google, LLC.
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
# [START run_events_pubsub_server_setup]
import base64
import os

from flask import Flask, request
app = Flask(__name__)
# [END run_events_pubsub_server_setup]

# [START run_events_pubsub_handler]


@app.route('/', methods=['GET'])
def hello_world():
    return 'GET Success!\n', 200


@app.route('/', methods=['POST'])
def event_handler():
    body = request.json

    if 'message' not in body or 'data' not in body['message']:
        msg = 'invalid Pub/Sub message format'
        return {'err': msg}, 400

    if 'ce-id' not in request.headers:
        msg = 'missing ce-id field in Pub/Sub headers'
        return {'err': msg}, 400

    base64_message = body['message']['data']
    name = base64.b64decode(base64_message).decode()

    return {'message': 'Hello {0}! ID: {1}'.format(
            name,
            request.headers['ce-id']
            )}, 200
# [END run_events_pubsub_handler]


# [START run_pubsub_server]
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
# [END run_pubsub_server]
