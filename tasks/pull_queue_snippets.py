#!/usr/bin/env python

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sample command-line program for interacting with the Cloud Tasks API.

See README.md for instructions on setting up your development environment
and running the scripts.
"""

import argparse
import base64


# [START cloud_tasks_create_task]
def create_task(project, queue, location):
    """Create a task for a given queue with an arbitrary payload."""

    import googleapiclient.discovery

    # Create a client.
    client = googleapiclient.discovery.build('cloudtasks', 'v2beta2')

    # Prepare the payload.
    payload = 'a message for the recipient'

    # The API expects base64 encoding of the payload, so encode the unicode
    # `payload` object into a byte string and base64 encode it.
    base64_encoded_payload = base64.b64encode(payload.encode())

    # The request body object will be emitted in JSON, which requires
    # unicode objects, so convert the byte string to unicode (still base64).
    converted_payload = base64_encoded_payload.decode()

    # Construct the request body.
    task = {
        'task': {
            'pullMessage': {
                'payload': converted_payload
            }
        }
    }

    # Construct the fully qualified queue name.
    queue_name = 'projects/{}/locations/{}/queues/{}'.format(
        project, location, queue)

    # Use the client to build and send the task.
    response = client.projects().locations().queues().tasks().create(
        parent=queue_name, body=task).execute()

    print('Created task {}'.format(response['name']))
    return response
# [END cloud_tasks_create_task]


# [START cloud_tasks_lease_and_acknowledge_task]
def lease_task(project, queue, location):
    """Lease a single task from a given queue for 10 minutes."""

    import googleapiclient.discovery

    # Create a client.
    client = googleapiclient.discovery.build('cloudtasks', 'v2beta2')

    duration_seconds = '600s'
    lease_options = {
        'maxTasks': 1,
        'leaseDuration': duration_seconds,
        'responseView': 'FULL'
    }

    queue_name = 'projects/{}/locations/{}/queues/{}'.format(
        project, location, queue)

    response = client.projects().locations().queues().tasks().lease(
        parent=queue_name, body=lease_options).execute()

    print('Leased task {}'.format(response))
    return response['tasks'][0]


def acknowledge_task(task):
    """Acknowledge a given task."""

    import googleapiclient.discovery

    # Create a client.
    client = googleapiclient.discovery.build('cloudtasks', 'v2beta2')

    body = {'scheduleTime': task['scheduleTime']}
    client.projects().locations().queues().tasks().acknowledge(
        name=task['name'], body=body).execute()

    print('Acknowledged task {}'.format(task['name']))
    # [END cloud_tasks_lease_and_acknowledge_task]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')

    create_task_parser = subparsers.add_parser(
        'create-task',
        help=create_task.__doc__)
    create_task_parser.add_argument(
        '--project',
        help='Project ID.',
        required=True,
    )
    create_task_parser.add_argument(
        '--queue',
        help='Queue ID (short name).',
        required=True,
    )
    create_task_parser.add_argument(
        '--location',
        help='Location of the queue, e.g. \'us-central1\'.',
        required=True,
    )

    lease_and_ack_parser = subparsers.add_parser(
        'lease-and-ack-task',
        help=create_task.__doc__)
    lease_and_ack_parser.add_argument(
        '--project',
        help='Project ID.',
        required=True,
    )
    lease_and_ack_parser.add_argument(
        '--queue',
        help='Queue ID (short name).',
        required=True,
    )
    lease_and_ack_parser.add_argument(
        '--location',
        help='Location of the queue, e.g. \'us-central1\'.',
        required=True,
    )

    args = parser.parse_args()

    if args.command == 'create-task':
        create_task(args.project, args.queue, args.location)
    if args.command == 'lease-and-ack-task':
        task = lease_task(args.project, args.queue, args.location)
        acknowledge_task(task)
