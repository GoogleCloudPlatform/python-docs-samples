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

from google.cloud import tasks


def create_queue(project, location, queue_blue_name, queue_red_name):
    # [START cloud_tasks_taskqueues_using_yaml]
    client = tasks.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us- central1'
    # queue_blue_name = 'queue-blue'
    # queue_red_name = 'queue-red'

    parent = f"projects/{project}/locations/{location}"

    queue_blue = {
        'name': client.queue_path(project, location, queue_blue_name),
        'rate_limits': {
            'max_dispatches_per_second': 5
        },
        'app_engine_routing_override': {
            'version': 'v2',
            'service': 'task-module'
        }
    }

    queue_red = {
        'name': client.queue_path(project, location, queue_red_name),
        'rate_limits': {
            'max_dispatches_per_second': 1
        }
    }

    queues = [queue_blue, queue_red]
    for queue in queues:
        response = client.create_queue(parent=parent, queue=queue)
        print(response)
    # [END cloud_tasks_taskqueues_using_yaml]
    return response


def update_queue(project, location, queue):
    # [START cloud_tasks_taskqueues_processing_rate]
    client = tasks.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us- central1'
    # queue = 'queue-blue'

    # Get queue object
    queue_path = client.queue_path(project, location, queue)
    queue = client.get_queue(name=queue_path)

    # Update queue object
    queue.rate_limits.max_dispatches_per_second = 20
    queue.rate_limits.max_concurrent_dispatches = 10

    response = client.update_queue(queue=queue)
    print(response)
    # [END cloud_tasks_taskqueues_processing_rate]
    return response


def create_task(project, location, queue):
    # [START cloud_tasks_taskqueues_new_task]
    client = tasks.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us- central1'
    # queue = 'default'
    amount = 10

    parent = client.queue_path(project, location, queue)

    task = {
        'app_engine_http_request': {
            'http_method': tasks.HttpMethod.POST,
            'relative_uri': '/update_counter',
            'app_engine_routing': {
                'service': 'worker'
            },
            'body': str(amount).encode()
        }
    }

    response = client.create_task(parent=parent, task=task)
    eta = response.schedule_time.strftime("%m/%d/%Y, %H:%M:%S")
    print('Task {} enqueued, ETA {}.'.format(response.name, eta))
    # [END cloud_tasks_taskqueues_new_task]
    return response


def create_tasks_with_data(project, location, queue):
    # [START cloud_tasks_taskqueues_passing_data]
    import json
    client = tasks.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us- central1'
    # queue = 'default'

    parent = client.queue_path(project, location, queue)

    task1 = {
        'app_engine_http_request': {
            'http_method': tasks.HttpMethod.POST,
            'relative_uri': '/update_counter?key=blue',
            'app_engine_routing': {
                'service': 'worker'
            }
        }
    }

    task2 = {
        'app_engine_http_request': {
            'http_method': tasks.HttpMethod.POST,
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

    response = client.create_task(parent=parent, task=task1)
    print(response)
    response = client.create_task(parent=parent, task=task2)
    print(response)
    # [END cloud_tasks_taskqueues_passing_data]
    return response


def create_task_with_name(project, location, queue, task_name):
    # [START cloud_tasks_taskqueues_naming_tasks]
    client = tasks.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us- central1'
    # queue = 'default'
    # task_name = 'first-try'

    parent = client.queue_path(project, location, queue)

    task = {
        'name': client.task_path(project, location, queue, task_name),
        'app_engine_http_request': {
            'http_method': tasks.HttpMethod.GET,
            'relative_uri': '/url/path'
        }
    }
    response = client.create_task(parent=parent, task=task)
    print(response)
    # [END cloud_tasks_taskqueues_naming_tasks]
    return response


def delete_task(project, location, queue):
    # [START cloud_tasks_taskqueues_deleting_tasks]
    client = tasks.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us- central1'
    # queue = 'queue1'

    task_path = client.task_path(project, location, queue, 'foo')
    response = client.delete_task(name=task_path)
    # [END cloud_tasks_taskqueues_deleting_tasks]
    return response


def purge_queue(project, location, queue):
    # [START cloud_tasks_taskqueues_purging_tasks]
    client = tasks.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us- central1'
    # queue = 'queue1'

    queue_path = client.queue_path(project, location, queue)
    response = client.purge_queue(name=queue_path)
    # [END cloud_tasks_taskqueues_purging_tasks]
    return response


def pause_queue(project, location, queue):
    # [START cloud_tasks_taskqueues_pause_queue]
    client = tasks.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us- central1'
    # queue = 'queue1'

    queue_path = client.queue_path(project, location, queue)
    response = client.pause_queue(name=queue_path)
    # [END cloud_tasks_taskqueues_pause_queue]
    return response


def delete_queue(project, location, queue):
    # [START cloud_tasks_taskqueues_deleting_queues]
    client = tasks.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us- central1'
    # queue = 'queue1'

    queue_path = client.queue_path(project, location, queue)
    response = client.delete_queue(name=queue_path)
    # [END cloud_tasks_taskqueues_deleting_queues]
    return response


def retry_task(project, location, fooqueue, barqueue, bazqueue):
    # [START cloud_tasks_taskqueues_retrying_tasks]
    from google.protobuf import duration_pb2

    client = tasks.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us- central1'
    # fooqueue = 'fooqueue'
    # barqueue = 'barqueue'
    # bazqueue = 'bazqueue'

    parent = f"projects/{project}/locations/{location}"

    max_retry = duration_pb2.Duration()
    max_retry.seconds = 2*60*60*24

    foo = {
        'name': client.queue_path(project, location, fooqueue),
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

    bar = {
        'name': client.queue_path(project, location, barqueue),
        'rate_limits': {
            'max_dispatches_per_second': 1
        },
        'retry_config': {
            'min_backoff': min,
            'max_backoff': max,
            'max_doublings': 0
        }
    }

    max.seconds = 300
    baz = {
        'name': client.queue_path(project, location, bazqueue),
        'rate_limits': {
            'max_dispatches_per_second': 1
        },
        'retry_config': {
            'min_backoff': min,
            'max_backoff': max,
            'max_doublings': 3
        }
    }

    queues = [foo, bar, baz]
    for queue in queues:
        response = client.create_queue(parent=parent, queue=queue)
        print(response)
    # [END cloud_tasks_taskqueues_retrying_tasks]
    return response
