# Copyright 2023 Google LLC
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


# [START cloud_tasks_create_http_queue]
import urllib

import google.protobuf
from google.cloud import tasks_v2beta3 as tasks


def create_http_queue(project: str, location: str, name: str, uri: str) -> tasks.Queue:
    """Create an HTTP queue.
    Args:
        project: The project ID to create the queue in.
        location: The location to create the queue in.
        name: The ID to use for the new queue.
        uri: The HTTP endpoint's URI for all tasks in the queue

    Returns:
        The newly created queue.
    """

    # Create a client.
    client = tasks.CloudTasksClient()

    # Create the HTTP Target for the queue. This property is required
    # for an HTTP queue. For legacy reasons, this property is an object
    # with multiple fields instead of a string containing a URI.

    # Extract the various components of the URI provided by the caller
    parsedUri = urllib.parse.urlparse(uri)

    http_target = {
        "uri_override": {
            "host": parsedUri.hostname,
            "uri_override_enforce_mode": 2,  # ALWAYS use this endpoint
        }
    }
    if parsedUri.scheme == "http":  # defaults to https
        http_target["uri_override"]["scheme"] = 1
    if parsedUri.port:
        http_target["uri_override"]["port"] = f"{parsedUri.port}"
    if parsedUri.path:
        http_target["uri_override"]["path_override"] = {"path": parsedUri.path}
    if parsedUri.query:
        http_target["uri_override"]["query_override"] = {
            "query_params": parsedUri.query
        }

    # Use the client to send a CreateQueueRequest.
    queue = client.create_queue(
        tasks.CreateQueueRequest(
            parent=client.common_location_path(project, location),
            queue={
                "name": f"projects/{project}/locations/{location}/queues/{name}",
                "http_target": http_target,
            },
        )
    )

    return queue


# [END cloud_tasks_create_http_queue]


# [START cloud_tasks_update_http_queue]
import google.protobuf
from google.cloud import tasks_v2beta3 as tasks


def update_http_queue(
    queue: tasks.Queue,
    uri: str = "",
    max_per_second: float = 0.0,
    max_burst: int = 0,
    max_concurrent: int = 0,
    max_attempts: int = 0,
) -> tasks.Queue:
    """Update an HTTP queue with provided properties.
    Args:
        queue: The queue to update.
        uri: The new HTTP endpoint
        max_per_second: the new maximum number of dispatches per second
        max_burst: the new maximum burst size
        max_concurrent: the new maximum number of concurrent dispatches
        max_attempts: the new maximum number of retries attempted
    Returns:
        The updated queue.
    """

    # Create a client.
    client = tasks.CloudTasksClient()

    update_mask = google.protobuf.field_mask_pb2.FieldMask(
        paths=[]
    )  # Track which fields need to be updated

    if uri:
        parsedUri = urllib.parse.urlparse(uri)

        http_target = {
            "uri_override": {
                "host": parsedUri.hostname,
                "uri_override_enforce_mode": 2,  # ALWAYS use this endpoint
            }
        }
        if parsedUri.scheme == "http":  # defaults to https
            http_target["uri_override"]["scheme"] = 1
        if parsedUri.port:
            http_target["uri_override"]["port"] = f"{parsedUri.port}"
        if parsedUri.path:
            http_target["uri_override"]["path_override"] = {"path": parsedUri.path}
        if parsedUri.query:
            http_target["uri_override"]["query_override"] = {
                "query_params": parsedUri.query
            }

        queue.http_target = http_target
        update_mask.paths.append("http_target")

    if max_per_second != 0.0:
        queue.rate_limits.max_dispatches_per_second = max_per_second
    if max_burst != 0:
        queue.rate_limits.max_burst_size = max_burst
    if max_concurrent != 0:
        queue.rate_limits.max_concurrent_dispatches = max_concurrent
    update_mask.paths.append("rate_limits")

    if max_attempts != 0:
        queue.retry_config.max_attempts = max_attempts
    update_mask.paths.append("retry_config")

    request = tasks.UpdateQueueRequest(queue=queue, update_mask=update_mask)
    updated_queue = client.update_queue(request)
    return updated_queue


# [END cloud_tasks_update_http_queue]


# [START cloud_tasks_delete_http_queue]
from google.cloud import tasks_v2beta3 as tasks


def delete_http_queue(
    queue: tasks.Queue,
) -> None:
    """Delete an HTTP queue.
    Args:
        queue: The queue to delete.
    Returns:
        None.
    """
    client = tasks.CloudTasksClient()
    client.delete_queue(name=queue.name)


# [END cloud_tasks_delete_http_queue]


# [START cloud_tasks_get_http_queue]
from google.cloud import tasks_v2beta3 as tasks


def get_http_queue(project: str, location: str, name: str) -> tasks.Queue:
    """Get an HTTP queue.
    Args:
        project: The project ID containing the queue.
        location: The location containing the queue.
        name: The ID of the queue.

    Returns:
        The matching queue, or None if it does not exist.
    """

    client = tasks.CloudTasksClient()
    return client.get_queue(
        name=f"projects/{project}/locations/{location}/queues/{name}"
    )


# [END cloud_tasks_get_http_queue]


# [START cloud_tasks_send_task_to_http_queue]
import requests

import google.auth
from google.auth.transport.requests import Request


def send_task_to_http_queue(
    queue: tasks.Queue, body: str = "", headers: dict = {}
) -> int:
    """Send a task to an HTTP queue.
    Args:
        queue: The queue to delete.
        body: the body of the task
        headers: headers to set on the task
    Returns:
        The matching queue, or None if it does not exist.
    """

    # Use application default credentials if not supplied in a header
    if "Authorization" not in headers:
        credentials, _ = google.auth.default()
        credentials.refresh(request=Request())
        headers["Authorization"] = f"Bearer {credentials.token}"

    endpoint = f"https://cloudtasks.googleapis.com/v2beta3/{queue.name}/tasks:buffer"
    response = requests.post(endpoint, body, headers=headers)

    return response.status_code


# [END cloud_tasks_send_task_to_http_queue]
