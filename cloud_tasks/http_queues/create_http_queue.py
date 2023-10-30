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

# HTTP Queues are currently in public beta
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
            "uri_override_enforce_mode": tasks.types.UriOverride.UriOverrideEnforceMode.ALWAYS,
        }
    }
    if parsedUri.scheme == "http":  # defaults to https
        http_target["uri_override"]["scheme"] = tasks.types.UriOverride.Scheme.HTTP
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
