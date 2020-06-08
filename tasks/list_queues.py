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


def list_queues(project,
                location):
    # [START cloud_tasks_list_queues]
    """List all task queues."""

    from google.cloud import tasks_v2

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Construct the fully qualified location path.
    parent = client.location_path(project, location)

    # Use the client to obtain the queues.
    response = client.list_queues(parent)

    # Convert the response to a list containing all queues.
    queue_list = list(response)

    # Print the results.
    for queue in queue_list:
        print(queue.name)

    return response
# [END cloud_tasks_list_queues]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=list_queues.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--project',
        help='Project to list queues for.',
        required=True,
    )

    parser.add_argument(
        '--location',
        help='Location of the project to list queues for.',
        required=True,
    )

    args = parser.parse_args()

    list_queues(
        args.project, args.location)
