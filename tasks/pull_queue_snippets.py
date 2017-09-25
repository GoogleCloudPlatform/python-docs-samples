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


def create_task(project, queue, location):
    """Create a task for a given queue with an arbitrary payload."""

    import googleapiclient.discovery

    # Create a client.
    client = googleapiclient.discovery.build('cloudtasks', 'v2beta2')

    payload = 'a message for the recipient'
    task = {
        'task': {
            'pull_message': {
                'payload': base64.b64encode(payload.encode()).decode()
            }
        }
    }

    queue_name = 'projects/{}/locations/{}/queues/{}'.format(
        project, location, queue)

    response = client.projects().locations().queues().tasks().create(
        parent=queue_name, body=task).execute()

    print('Created task {}'.format(response['name']))
    return response


def pull_task(project, queue, location):
    """Pull a single task from a given queue and lease it for 10 minutes."""

    import googleapiclient.discovery

    # Create a client.
    client = googleapiclient.discovery.build('cloudtasks', 'v2beta2')

    duration_seconds = '600s'
    pull_options = {
        'max_tasks': 1,
        'leaseDuration': duration_seconds,
        'responseView': 'FULL'
    }

    queue_name = 'projects/{}/locations/{}/queues/{}'.format(
        project, location, queue)

    response = client.projects().locations().queues().tasks().pull(
        name=queue_name, body=pull_options).execute()

    print('Pulled task {}'.format(response))
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
        help='Project of the queue to add the task to.',
        required=True,
    )
    create_task_parser.add_argument(
        '--queue',
        help='ID (short name) of the queue to add the task to.',
        required=True,
    )
    create_task_parser.add_argument(
        '--location',
        help='Location of the queue to add the task to.',
        required=True,
    )

    pull_and_ack_parser = subparsers.add_parser(
        'pull-and-ack-task',
        help=create_task.__doc__)
    pull_and_ack_parser.add_argument(
        '--project',
        help='Project of the queue to pull the task from.',
        required=True,
    )
    pull_and_ack_parser.add_argument(
        '--queue',
        help='ID (short name) of the queue to pull the task from.',
        required=True,
    )
    pull_and_ack_parser.add_argument(
        '--location',
        help='Location of the queue to pull the task from.',
        required=True,
    )

    args = parser.parse_args()

    if args.command == 'create-task':
        create_task(args.project, args.queue, args.location)
    if args.command == 'pull-and-ack-task':
        task = pull_task(args.project, args.queue, args.location)
        acknowledge_task(task)
