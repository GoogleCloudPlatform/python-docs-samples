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

# [START cloudtasks_pushcounter]
"""A simple counter with a Pub/Sub push subscription, replacing a
   TaskQueue push queue, which is not available in Python 3 App Engine
   runtimes.
"""

import logging
import os

from flask import Flask, redirect, render_template, request
from google.cloud import datastore
from google.cloud import tasks_v2 as tasks


app = Flask(__name__)
datastore_client = datastore.Client()
client = tasks.CloudTasksClient()


queue_name = os.environ.get('QUEUE', 'queue')
location = os.environ.get('LOCATION', 'us-central1')
project = os.environ['GOOGLE_CLOUD_PROJECT']
queue = 'projects/{}/locations/{}/queues/{}'.format(
    project, location, queue_name
)
entity_kind = os.environ.get('ENTITY_KIND', 'Task')


def increment_counter(id):
    with datastore_client.transaction():
        key = datastore_client.key(entity_kind, id)
        task = datastore_client.get(key)
        if not task:
            task_key = datastore_client.key(entity_kind, id)
            task = datastore.Entity(key=task_key)
            task['count'] = 0

        task['count'] += 1
        datastore_client.put(task)


@app.route('/', methods=['GET'])
def home_page():
    query = datastore_client.query(kind=entity_kind)
    counters = [
        {
            'name': entity.key.name,
            'count': entity['count']
        } for entity in query.fetch()
    ]
    return render_template('counter.html', counters=counters)


@app.route('/', methods=['POST'])
def enqueue():
    key = request.form.get('key', None)
    if key is not None:
        # Method definition moved between library versions
        try:
            method = tasks.HttpMethod.POST
        except AttributeError:
            method = tasks.enums.HttpMethod.POST

        task = {
            'app_engine_http_request': {
                'http_method': method,
                'relative_uri': '/push-task',
                'body': key.encode()
            }
        }
        client.create_task(parent=queue, task=task)

    return redirect('/')


@app.route('/push-task', methods=['POST'])
def handle_task():
    # App Engine runtime will add X-AppEngine-QueueName headers to Cloud Tasks
    # requests, and strip such headers from any other source.
    queue_header = request.headers.get('X-AppEngine-QueueName')
    if queue_header != queue_name:
        logging.error('Missing or wrong queue name: {}'.format(queue_header))
        # Return a 200 status response, so sender doesn't keep retrying, but
        # include the fact that it was rejected in the response for debugging.
        return 'REJECTED'

    key = request.get_data(as_text=True)
    if key is not None:
        increment_counter(key)

    return 'OK'
# [END cloudtasks_pushcounter]


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
