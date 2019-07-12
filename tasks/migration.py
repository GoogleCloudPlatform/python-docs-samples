
from google.cloud import tasks
from google.protobuf import timestamp_pb2
from google.protobuf import duration_pb2
import json

# Create a client.
client = tasks.CloudTasksClient()

project = 'my-project-id'
location = 'us-central1'

# [START taskqueues_using_yaml]
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

## Create Queue
queues = [queue_blue, queue_red]
for queue in queues:
    response = client.create_queue(parent, queue)
    print(response)
# [END taskqueues_using_yaml]


# [START taskqueues_processing_rate]
# Get queue object
queue_path = client.queue_path(project, location, 'queue-blue')
queue = client.get_queue(queue_path)

# Update queue object
queue.rate_limits.max_dispatches_per_second = 20
queue.rate_limits.max_concurrent_dispatches = 10

# Send update request
response = client.update_queue(queue)
print(response)
# [END taskqueues_processing_rate]


# [START taskqueues_new_task]
amount = '10'.encode()
queue = 'default'

# Construct the fully qualified queue name.
parent = client.queue_path(project, location, queue)

# Construct the request body.
task = {
    'app_engine_http_request': {
        'http_method': 'POST',
        'relative_uri': '/update_counter',
        'app_engine_routing': {
            'service': 'worker'
        },
        'body': amount
    }
}

# Use the client to build and send the task.
response = client.create_task(parent, task)

eta = response.schedule_time.ToDatetime().strftime("%m/%d/%Y, %H:%M:%S")
print('Task {} enqueued, ETA {}.'.format(response.name, eta))
# [END taskqueues_new_task]

# [START taskqueues_passing_data]
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

# Use the client to build and send the task.
tasks = [task1, task2]
for task in tasks:
    response = client.create_task(parent, task)
    print(response)
# [END taskqueues_passing_data]

# [START taskqueues_naming_tasks]
task = {
    'name': client.task_path(project, location, queue, 'first-try'),
    'app_engine_http_request': {
        'http_method': 'GET',
        'relative_uri': '/url/path'
    }
}
response = client.create_task(parent, task)
print(response)
# [END taskqueues_naming_tasks]

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

# [START taskqueues_retrying_tasks]
from google.protobuf import duration_pb2

fooqueue = {
    'name': client.queue_path(project, location, 'fooqueue'),
    'rate_limits': {
        'max_dispatches_per_second': 1
    },
    'retry_config': {
        'max_attempts': 7,
        'max_retry_duration': 2*60*60*24
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

## Create Queue
queues = [fooqueue, barqueue, bazqueue]
for queue in queues:
    response = client.create_queue(parent, queue)
    print(response)
# [END taskqueues_retrying_tasks]
