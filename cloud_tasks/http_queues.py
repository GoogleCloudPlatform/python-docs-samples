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

import urllib

from google.cloud import tasks_v2beta3 as tasks


# [START cloud_tasks_create_http_queue]
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

    parsedUri = urllib.parse.urlparse(uri)
    parent = client.common_location_path(project, location)
    queue = {
        #"name": name,
        "name": f"projects/{project}/locations/{location}/queues/{name}",
        "http_target": {
            "uri_override": {
                #"scheme": parsedUri.scheme,
                "host": parsedUri.hostname,
            }
        },
    }

    uri_override = queue["http_target"]["uri_override"]

    if parsedUri.path:
        uri_override["path_override"] = {"path": parsedUri.path}

    if parsedUri.query:
        uri_override["query_override"] = {"query_params": parsedUri.query}

    # Use the client to send a CreateQueueRequest.
    return client.create_queue(
        tasks.CreateQueueRequest(
            parent=parent,
            queue=queue,
        )
    )


# [END cloud_tasks_create_http_queue]


# [START cloud_tasks_update_http_queue]
def update_http_queue(queue: tasks.Queue, uri: str = "") -> tasks.Queue:
    """Create an HTTP queue.
    Args:
        queue: The queue to update.
        endpoint: The new HTTP endpoint's URI for all tasks in the queue

    Returns:
        The updated queue.
    """
    
    #TODO

# [END cloud_tasks_update_http_queue]


# [START cloud_tasks_delete_http_queue]
# [END cloud_tasks_delete_http_queue]


# [START cloud_tasks_describe_http_queue]
# [END cloud_tasks_describe_http_queue]


# [START cloud_tasks_send_task_to_http_queue]
# [END cloud_tasks_send_task_to_http_queue]
