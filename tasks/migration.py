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

from google.cloud import tasks

def create_queue():
    # [START taskqueues_using_yaml]
    client = tasks.CloudTasksClient()

    project = 'my-project-id'
    location = 'us-central1'
    parent = client.location_path(project, location)

    queue_blue = {
        'name': client.queue_path(project, location, 'queue-blue'),
        'rate_limits': {
            'max_dispatches_per_second': 5
        },
        'app_engine_routing_override': {
            'version': 'v2',
            'service': 'task-module'
        }
    }

    queue_red = {
        'name': client.queue_path(project, location, 'queue-red'),
        'rate_limits': {
            'max_dispatches_per_second': 1
        }
    }

    queues = [queue_blue, queue_red]
    for queue in queues:
        response = client.create_queue(parent, queue)
        print(response)
    # [END taskqueues_using_yaml]


def update_queue():
    # [START taskqueues_processing_rate]
    client = tasks.CloudTasksClient()

    project = 'my-project-id'
    location = 'us-central1'

    # Get queue object
    queue_path = client.queue_path(project, location, 'queue-blue')
    queue = client.get_queue(queue_path)

    # Update queue object
    queue.rate_limits.max_dispatches_per_second = 20
    queue.rate_limits.max_concurrent_dispatches = 10

    response = client.update_queue(queue)
    print(response)
    # [END taskqueues_processing_rate]


def create_task():
    # [START taskqueues_new_task]
    client = tasks.CloudTasksClient()

    project = 'my-project-id'
    location = 'us-central1'
    queue = 'default'
    amount = 10
    parent = client.queue_path(project, location, queue)

    task = {
        'app_engine_http_request': {
            'http_method': 'POST',
            'relative_uri': '/update_counter',
            'app_engine_routing': {
                'service': 'worker'
            },
            'body': str(amount).encode()
        }
    }

    response = client.create_task(parent, task)
    eta = response.schedule_time.ToDatetime().strftime("%m/%d/%Y, %H:%M:%S")
    print('Task {} enqueued, ETA {}.'.format(response.name, eta))
    # [END taskqueues_new_task]

def create_tasks_with_data():
    # [START taskqueues_passing_data]
    import json
    client = tasks.CloudTasksClient()

    project = 'my-project-id'
    location = 'us-central1'
    queue = 'default'
    parent = client.queue_path(project, location, queue)

    task1 = {
        'app_engine_http_request': {
            'http_method': 'POST',
            'relative_uri': '/update_counter?key=blue',
            'app_engine_routing': {
                'service': 'worker'
            }
        }
    }

    task2 = {
        'app_engine_http_request': {
            'http_method': 'POST',
            'relative_uri': '/update_counter',
            'app_engine_routing': {
                'service': 'worker'
            },
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'key': 'blue'}).encode()
        }
    }

    tasks = [task1, task2]
    for task in tasks:
        response = client.create_task(parent, task)
        print(response)
    # [END taskqueues_passing_data]


def create_task_with_name():
    # [START taskqueues_naming_tasks]
    client = tasks.CloudTasksClient()

    project = 'my-project-id'
    location = 'us-central1'
    queue = "default"
    parent = client.queue_path(project, location, queue)

    task =  {
        'name': client.task_path(project, location, queue, 'first-try'),
        'app_engine_http_request': {
            'http_method': 'GET',
            'relative_uri': '/url/path'
        }
    }
    response = client.create_task(parent, task)
    print(response)
    # [END taskqueues_naming_tasks]


def delete_tasks():
    # [START taskqueues_setup]
    client = tasks.CloudTasksClient()

    project = 'my-project-id'
    location = 'us-central1'
    # [START taskqueues_setup]

    # [START taskqueues_deleting_tasks]
    task_path = client.task_path(project, location, 'queue1', 'foo')
    response = client.delete_task(task_path)
    # [END taskqueues_deleting_tasks]

    # [START taskqueues_purging_tasks]
    queue_path = client.queue_path(project, location, 'queue1')
    response = client.purge_queue(queue_path)
    # [END taskqueues_purging_tasks]

    # [START taskqueues_pause_queue]
    queue_path = client.queue_path(project, location, 'queue1')
    response = client.pause_queue(queue_path)
    # [END taskqueues_pause_queues]

    # [START taskqueues_deleting_queues]
    queue_path = client.queue_path(project, location, 'queue1')
    response = client.delete_queue(queue_path)
    # [END taskqueues_deleting_queues]


def retry_task():
    # [START taskqueues_retrying_tasks]
    from google.protobuf import duration_pb2

    client = tasks.CloudTasksClient()

    project = 'my-project-id'
    location = 'us-central1'
    parent = client.location_path(project, location)

    max_retry = duration_pb2.Duration()
    max_retry.seconds = 2*60*60*24

    fooqueue = {
        'name': client.queue_path(project, location, 'fooqueue'),
        'rate_limits': {
            'max_dispatches_per_second': 1
        },
        'retry_config': {
            'max_attempts': 7,
            'max_retry_duration': max_retry
        }
    }

    min = duration_pb2.Duration()
    min.seconds = 10

    max = duration_pb2.Duration()
    max.seconds = 200

    barqueue = {
        'name': client.queue_path(project, location, 'barqueue'),
        'rate_limits': {
            'max_dispatches_per_second': 1
        },
        'retry_config': {
            'min_backoff': min,
            'max_backoff': max,
            'nax_doublings': 0
        }
    }

    max.seconds = 300
    bazqueue = {
        'name': client.queue_path(project, location, 'bazqueue'),
        'rate_limits': {
            'max_dispatches_per_second': 1
        },
        'retry_config': {
            'min_backoff': min,
            'max_backoff': max,
            'nax_doublings': 3
        }
    }

    queues = [fooqueue, barqueue, bazqueue]
    for queue in queues:
        response = client.create_queue(parent, queue)
        print(response)
    # [END taskqueues_retrying_tasks]
