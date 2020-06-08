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


def delete_queue(project,
                 queue_name,
                 location):
    # [START cloud_tasks_delete_queue]
    """Delete a task queue."""

    from google.cloud import tasks_v2
    from google.api_core import exceptions

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Get the fully qualified path to queue.
    queue = client.queue_path(project, location, queue_name)

    # Use the client to delete the queue.
    try:
        client.delete_queue(queue)
        print('Deleted queue')
    except exceptions.NotFound:
        print('Queue not found')

# [END cloud_tasks_delete_queue]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=delete_queue.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--project',
        help='Project to delete the queue from.',
        required=True,
    )

    parser.add_argument(
        '--queue',
        help='ID (short name) of the queue to be deleted.',
        required=True,
    )

    parser.add_argument(
        '--location',
        help='Location of the queue.',
        required=True,
    )

    args = parser.parse_args()

    delete_queue(
        args.project, args.queue, args.location)
