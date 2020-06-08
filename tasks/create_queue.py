# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import argparse


def create_queue(project,
                 queue_name,
                 location):
    # [START cloud_tasks_create_queue]
    """Create a task queue."""

    from google.cloud import tasks_v2

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Construct the fully qualified location path.
    parent = client.location_path(project, location)

    # Construct the queue.
    queue = {
        'name': client.queue_path(project, location, queue_name)
    }

    # Use the client to create the queue.
    response = client.create_queue(parent, queue)

    print('Created queue {}'.format(response.name))
    return response
# [END cloud_tasks_create_queue]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=create_queue.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--project',
        help='Project to add the queue to.',
        required=True,
    )

    parser.add_argument(
        '--queue',
        help='ID (short name) of the queue to be created.',
        required=True,
    )

    parser.add_argument(
        '--location',
        help='Location of the project to add the queue to.',
        required=True,
    )

    args = parser.parse_args()

    create_queue(
        args.project, args.queue, args.location)
