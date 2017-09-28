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


def seconds_from_now_to_rfc3339_datetime(seconds):
    """Return an RFC 3339 datetime string for a number of seconds from now."""
    d = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
    return d.isoformat('T') + 'Z'


def create_task(project, queue, location, payload=None, in_seconds=None):
    """Create a task for a given queue with an arbitrary payload."""

    import googleapiclient.discovery

    # Create a client.
    client = googleapiclient.discovery.build('cloudtasks', 'v2beta2')

    url = '/log_payload'
    body = {
        'task': {
            'app_engine_http_request': {
                'http_method': 'POST',
                'relative_url': url
            }
        }
    }

    if payload is not None:
        # Payload is a string (unicode), and must be encoded for base64.
        # The finished request body is JSON, which requires unicode.
        body['task']['app_engine_http_request']['payload'] = base64.b64encode(
            payload.encode()).decode()

    if in_seconds is not None:
        scheduled_time = seconds_from_now_to_rfc3339_datetime(in_seconds)
        body['task']['schedule_time'] = scheduled_time

    queue_name = 'projects/{}/locations/{}/queues/{}'.format(
        project, location, queue)

    print('Sending task {}'.format(json.dumps(body)))

    response = client.projects().locations().queues().tasks().create(
        parent=queue_name, body=body).execute()

    print('Created task {}'.format(response['name']))
    return response


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
        '--in_seconds',
        help='The number of seconds from now to schedule task attempt.'
    )

    args = parser.parse_args()

    create_task(
        args.project, args.queue, args.location,
        args.payload, args.in_seconds)
