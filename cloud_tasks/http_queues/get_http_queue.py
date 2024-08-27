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
