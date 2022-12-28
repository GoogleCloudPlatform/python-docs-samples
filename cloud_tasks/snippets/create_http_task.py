#!/usr/bin/env python
#
# Copyright 2022 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import argparse


def create_http_task(
    project,
    queue,
    location,
    url,
    payload=None,
    in_seconds=None,
    task_name=None,
    deadline=None,
):
    # [START cloud_tasks_create_http_task]
    """Create a task for a given queue with an arbitrary payload."""

    import datetime
    import json

    from google.cloud import tasks_v2
    from google.protobuf import duration_pb2, timestamp_pb2

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # queue = 'my-queue'
    # location = 'us-central1'
    # url = 'https://example.com/task_handler'
    # payload = 'hello' or {'param': 'value'} for application/json
    # in_seconds = 180
    # task_name = 'my-unique-task'
    # deadline = 900

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,  # The full url path that the task will be sent to.
        }
    }
    if payload is not None:
        if isinstance(payload, dict):
            # Convert dict to JSON string
            payload = json.dumps(payload)
            # specify http content-type to application/json
            task["http_request"]["headers"] = {"Content-type": "application/json"}

        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task["http_request"]["body"] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

        # Create Timestamp protobuf.
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)

        # Add the timestamp to the tasks.
        task["schedule_time"] = timestamp

    if task_name is not None:
        # Add the name to tasks.
        task["name"] = client.task_path(project, location, queue, task_name)

    if deadline is not None:
        # Add dispatch deadline for requests sent to the worker.
        duration = duration_pb2.Duration()
        duration.FromSeconds(deadline)
        task["dispatch_deadline"] = duration

    # Use the client to build and send the task.
    response = client.create_task(request={"parent": parent, "task": task})

    print("Created task {}".format(response.name))
    # [END cloud_tasks_create_http_task]
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=create_http_task.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--project",
        help="Project of the queue to add the task to.",
        required=True,
    )

    parser.add_argument(
        "--queue",
        help="ID (short name) of the queue to add the task to.",
        required=True,
    )

    parser.add_argument(
        "--location",
        help="Location of the queue to add the task to.",
        required=True,
    )

    parser.add_argument(
        "--url",
        help="The full url path that the request will be sent to.",
        required=True,
    )

    parser.add_argument(
        "--payload", help="Optional payload to attach to the push queue."
    )

    parser.add_argument(
        "--in_seconds",
        type=int,
        help="The number of seconds from now to schedule task attempt.",
    )

    parser.add_argument("--task_name", help="Task name of the task to create")
    args = parser.parse_args()

    create_http_task(
        args.project,
        args.queue,
        args.location,
        args.url,
        args.payload,
        args.in_seconds,
        args.task_name,
    )
