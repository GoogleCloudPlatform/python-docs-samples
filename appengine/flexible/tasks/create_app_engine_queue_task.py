# Copyright 2019 Google LLC.
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


import argparse


def create_task(project, queue, location, payload=None, in_seconds=None):
    # [START cloud_tasks_appengine_create_task]
    """Create a task for a given queue with an arbitrary payload."""

    from google.cloud import tasks_v2
    from google.protobuf import timestamp_pb2
    import datetime
    import json

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # queue = 'my-appengine-queue'
    # location = 'us-central1'
    # payload = 'hello' or {'param': 'value'} for application/json
    # in_seconds = None

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
            'app_engine_http_request': {  # Specify the type of request.
                'http_method': tasks_v2.HttpMethod.POST,
                'relative_uri': '/example_task_handler'
            }
    }
    if payload is not None:
        if isinstance(payload, dict):
            # Convert dict to JSON string
            payload = json.dumps(payload)
            # specify http content-type to application/json
            task["app_engine_http_request"]["headers"] = {"Content-type": "application/json"}
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task['app_engine_http_request']['body'] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        d = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=in_seconds)

        # Create Timestamp protobuf.
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)

        # Add the timestamp to the tasks.
        task['schedule_time'] = timestamp

    # Use the client to build and send the task.
    response = client.create_task(parent=parent, task=task)

    print(f'Created task {response.name}')
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
