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

# [START all]
"""A simple counter with a Pub/Sub pull subscription, replacing a
   TaskQueue pull queue, which is not available in Python 3 App Engine
   runtimes.
"""

import os
import time

from flask import Flask, redirect, render_template, request
from google.cloud import datastore
from google.cloud import pubsub_v1 as pubsub


app = Flask(__name__)
datastore_client = datastore.Client()
publisher = pubsub.PublisherClient()
subscriber = pubsub.SubscriberClient()

topic_name = os.environ.get('TOPIC', 'queue')
sub_name = os.environ.get('SUBSCRIPTION', 'tasklist')
project = os.environ['GOOGLE_CLOUD_PROJECT']
topic = 'projects/{}/topics/{}'.format(project, topic_name)
subscription = 'projects/{}/subscriptions/{}'.format(project, sub_name)

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
        publisher.publish(topic, b'', key=key)
    return redirect('/')


def processing_tasks():
    """Task processing normally runs continually when triggered by a GET
       request to /_ah/start. In order to make this more testable, we
       process tasks until this method returns False, which can only happen
       if this method is overridden by the tests.
    """
    return True


@app.route('/_ah/start')
def start_handling_tasks():
    """Indefinitely fetch tasks and update the datastore."""
    while processing_tasks():
        response = subscriber.pull(
            subscription=subscription,
            max_messages=5,
            timeout=60.0
        )
        for msg in response.received_messages:
            key = msg.message.attributes.get('key', None)
            if key is not None:
                increment_counter(key)
            subscriber.acknowledge(
                subscription=subscription,
                ack_ids=[msg.ack_id]
            )

        time.sleep(1)

    return 'Done'   # Never reached except under test
# [END all]


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
