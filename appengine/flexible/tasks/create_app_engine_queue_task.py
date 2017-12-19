# Copyright 2017 Google Inc. All Rights Reserved.
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

from __future__ import print_function

import argparse
import base64
import datetime
import json


# [START cloud_tasks_appengine_create_task]
def create_task(project, queue, location, payload=None, in_seconds=None):
    """Create a task for a given queue with an arbitrary payload."""

    import googleapiclient.discovery

    # Create a client.
    client = googleapiclient.discovery.build('cloudtasks', 'v2beta2')

    # Construct the request body.
    url = '/example_task_handler'
    body = {
        'task': {
            'appEngineHttpRequest': {  # Specify the type of request.
                'httpMethod': 'POST',
                'relativeUrl': url
            }
        }
    }

    if payload is not None:
        # The API expects base64 encoding of the payload, so encode the unicode
        # `payload` object into a byte string and base64 encode it.
        base64_encoded_payload = base64.b64encode(payload.encode())

        # The request body object will be emitted in JSON, which requires
        # unicode objects, so convert the byte string to unicode, still base64.
        converted_payload = base64_encoded_payload.decode()

        # Add the payload to the request.
        body['task']['appEngineHttpRequest']['payload'] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)
        scheduled_time = d.isoformat('T') + 'Z'

        # Add the rfc3339 datetime string to the request.
        body['task']['scheduleTime'] = scheduled_time

    # Construct the fully qualified queue name.
    queue_name = 'projects/{}/locations/{}/queues/{}'.format(
        project, location, queue)

    print('Sending task {}'.format(json.dumps(body)))

    # Use the client to build and send the task.
    response = client.projects().locations().queues().tasks().create(
        parent=queue_name, body=body).execute()

    print('Created task {}'.format(response['name']))
    return response
# [END cloud_tasks_appengine_create_task]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=create_task.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--project',
        help='Project of the queue to add the task to.',
        required=True,
    )

    parser.add_argument(
        '--queue',
        help='ID (short name) of the queue to add the task to.',
        required=True,
    )

    parser.add_argument(
        '--location',
        help='Location of the queue to add the task to.',
        required=True,
    )

    parser.add_argument(
        '--payload',
        help='Optional payload to attach to the push queue.'
    )

    parser.add_argument(
        '--in_seconds', type=int,
        help='The number of seconds from now to schedule task attempt.'
    )

    args = parser.parse_args()

    create_task(
        args.project, args.queue, args.location,
        args.payload, args.in_seconds)
