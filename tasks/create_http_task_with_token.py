# Copyright 2019 Google LLC All Rights Reserved.
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

import datetime


def create_http_task(project,
                     queue,
                     location,
                     url,
                     service_account_email,
                     payload=None,
                     in_seconds=None,
                     task_name=None):
    # [START cloud_tasks_create_http_task_with_token]
    """Create a task for a given queue with an arbitrary payload."""

    from google.cloud import tasks_v2
    from google.protobuf import timestamp_pb2

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # queue = 'my-queue'
    # location = 'us-central1'
    # url = 'https://example.com/task_handler'
    # payload = 'hello'

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
            'http_request': {  # Specify the type of request.
                'http_method': 'POST',
                'url': url,  # The full url path that the task will be sent to.
                'oidc_token': {
                    'service_account_email': service_account_email
                }
            }
    }

    if payload is not None:
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task['http_request']['body'] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

        # Create Timestamp protobuf.
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)

        # Add the timestamp to the tasks.
        task['schedule_time'] = timestamp

    if task_name is not None:
        # Add the name to tasks.
        task['name'] = task_name

    # Use the client to build and send the task.
    response = client.create_task(parent, task)

    print('Created task {}'.format(response.name))
    return response
# [END cloud_tasks_create_http_task_with_token]
