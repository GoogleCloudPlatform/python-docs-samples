# Copyright 2016 Google Inc. All Rights Reserved.
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
import base64
import datetime

from googleapiclient import discovery


def format_rfc3339(datetime_instance):
    """Format a datetime per RFC 3339."""
    return datetime_instance.isoformat("T") + "Z"


def get_seconds_from_now_rfc3339(seconds):
    """Return seconds from the current time as a RFC 3339 string."""
    d = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
    return format_rfc3339(d)


def list_queues(api_key, project_id, location_id):
    """List the queues in the location."""
    client = get_client(api_key)
    parent = 'projects/{}/locations/{}'.format(project_id, location_id)
    queues = []
    next_page_token = None

    while True:
        response = client.projects().locations().queues().list(
            parent=parent, pageToken=next_page_token).execute()
        queues += response['queues']
        if next_page_token is None:
            break

    print('Listing queues for location {}'.format(location_id))

    for queue in response['queues']:
        print queue['name']
    return response


def create_task(api_key, queue_name, payload=None, in_seconds=None):
    """Create a task for a given queue with an arbitrary payload."""
    client = get_client(api_key)

    url = '/set_payload'
    task = {
        'task': {
            'app_engine_task_target': {
                'http_method': 'POST',
                'relative_url': url
            }
        }
    }

    if payload is not None:
        task['task']['app_engine_task_target']['payload'] = base64.b64encode(
            payload)

    if in_seconds is not None:
        scheduled_time = get_seconds_from_now_rfc3339(int(in_seconds))
        task['task']['schedule_time'] = scheduled_time

    print('Sending task {}'.format(task))

    response = client.projects().locations().queues().tasks().create(
        parent=queue_name, body=task).execute()

    # By default CreateTaskRequest.responseView is BASIC, so not all
    # information is retrieved by default because some data, such as payloads,
    # might be desirable to return only when needed because of its large size
    # or because of the sensitivity of data that it contains.
    print('Created task {}'.format(response['name']))
    return response


def get_client(api_key):
    """Build an authenticated http client."""
    DISCOVERY_URL = 'https://cloudtasks.googleapis.com/$discovery/rest?version=v2beta2&key={}'.format(
        api_key)
    client = discovery.build('cloudtasks', 'v2beta2',
                             discoveryServiceUrl=DISCOVERY_URL)
    return client


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--api_key', help='API Key', required=True)

    subparsers = parser.add_subparsers(dest='command')

    list_queues_parser = subparsers.add_parser(
        'list-queues',
        help=list_queues.__doc__)

    list_queues_parser.add_argument(
        '--project_id',
        help='Project ID you want to access.',
        required=True)

    list_queues_parser.add_argument(
        '--location_id',
        help='Location of the queues.',
        required=True)

    create_task_parser = subparsers.add_parser(
        'create-task',
        help=create_task.__doc__)
    create_task_parser.add_argument(
        '--queue_name',
        help='Fully qualified name of the queue to add the task to.'
    )

    create_task_parser.add_argument(
        '--payload',
        help='Optional payload to attach to the push queue.'
    )

    create_task_parser.add_argument(
        '--in_seconds',
        help='The number of seconds from now to schedule task attempt.'
    )

    args = parser.parse_args()

    if args.command == 'list-queues':
        list_queues(args.api_key, args.project_id, args.location_id)
    if args.command == 'create-task':
        create_task(args.api_key, args.queue_name, args.payload, args.in_seconds)
