#!/usr/bin/env python

# Copyright 2018 Google Inc.
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


def create_task(project, queue, location):
    # [START cloud_tasks_create_task]
    """Create a task for a given queue with an arbitrary payload."""

    from google.cloud import tasks_v2beta2

    # Create a client.
    client = tasks_v2beta2.CloudTasksClient()

    # Prepare the payload of type bytes.
    payload = 'a message for the recipient'.encode()

    # Construct the request body.
    task = {
        'pull_message': {
            'payload': payload,
        }
    }

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Use the client to build and send the task.
    response = client.create_task(parent, task)

    print('Created task: {}'.format(response.name))
    return response
    # [END cloud_tasks_create_task]


def lease_task(project, queue, location):
    # [START cloud_tasks_lease_and_acknowledge_task]
    """Lease a single task from a given queue for 10 minutes."""

    from google.cloud import tasks_v2beta2

    # Create a client.
    client = tasks_v2beta2.CloudTasksClient()

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    lease_duration = {'seconds': 600}

    # Send lease request to client.
    response = client.lease_tasks(
        parent, lease_duration, max_tasks=1, response_view='FULL')

    task = response.tasks[0]

    print('Leased task {}'.format(task.name))
    return task


def acknowledge_task(task):
    """Acknowledge a given task."""

    from google.cloud import tasks_v2beta2

    # Create a client.
    client = tasks_v2beta2.CloudTasksClient()

    # Send request to client to acknowledge task.
    client.acknowledge_task(task.name, task.schedule_time)

    print('Acknowledged task {}'.format(task.name))
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
