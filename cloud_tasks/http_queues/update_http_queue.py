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


# [START cloud_tasks_update_http_queue]
import urllib

# HTTP Queues are currently in public beta
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

    # Track which fields need to be updated
    update_mask = {"paths": []}

    if uri:
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

        queue.http_target = http_target
        update_mask["paths"].append("http_target")

    # Update values only if the arguments are not the default values.
    if max_per_second != 0.0:
        queue.rate_limits.max_dispatches_per_second = max_per_second
    if max_burst != 0:
        queue.rate_limits.max_burst_size = max_burst
    if max_concurrent != 0:
        queue.rate_limits.max_concurrent_dispatches = max_concurrent
    update_mask["paths"].append("rate_limits")

    if max_attempts != 0:
        queue.retry_config.max_attempts = max_attempts
    update_mask["paths"].append("retry_config")

    request = tasks.UpdateQueueRequest(queue=queue, update_mask=update_mask)
    updated_queue = client.update_queue(request)
    return updated_queue


# [END cloud_tasks_update_http_queue]
