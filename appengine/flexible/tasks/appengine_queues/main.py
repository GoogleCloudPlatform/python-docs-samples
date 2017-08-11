# Copyright 2016 Google Inc.
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

"""App Engine app to serve as an endpoint for App Engine queue samples."""

from google.cloud import datastore
from flask import Flask, request

app = Flask(__name__)
client = datastore.Client()


def get_payload_from_datastore():
    payload_key = client.key('Payload', 1)
    payload_entity = client.get(payload_key)
    if payload_entity is None:
        return None
    return payload_entity['value']


def get_counter_from_datastore():
    counter_key = client.key('Counter', 1)
    counter_entity = client.get(counter_key)
    if counter_entity is None:
        return 0
    return counter_entity['counter']


def update_payload(request_data):
    """Sets the payload value entity in Cloud Datastore."""
    payload_key = client.key('Payload', 1)
    payload_entity = datastore.Entity(payload_key)

    if request_data:
        payload_entity['value'] = request_data
        client.put(payload_entity)

    payload_entity = client.get(payload_key)
    return payload_entity['value']


def increment_counter():
    """Increments a counter value in Cloud Datastore."""
    counter_key = client.key('Counter', 1)
    counter_entity = client.get(counter_key)
    if counter_entity is None:
        counter_entity = datastore.Entity(counter_key)
        counter_entity['counter'] = 0
        client.put(counter_entity)

    counter_entity['counter'] += 1
    client.put(counter_entity)
    return counter_entity['counter']


@app.route('/set_payload', methods=['POST'])
def set_payload():
    """Main endpoint to demonstrate Cloud Tasks App Engine queue features."""
    counter = increment_counter()
    payload = update_payload(request.data)

    return 'Counter value is now {}, payload value is now {}'.format(
        counter, payload)


@app.route('/get_payload')
def get_payload():
    """Main endpoint to demonstrate Cloud Tasks App Engine queue features."""
    counter = get_counter_from_datastore()
    payload = get_payload_from_datastore()

    return 'Counter value is now {}, payload value is now {}'.format(
        counter, payload)


@app.route('/')
def hello():
    """Basic index to verify app is serving."""
    return 'Hello World!'


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
