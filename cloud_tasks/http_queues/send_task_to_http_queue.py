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


# [START cloud_tasks_send_task_to_http_queue]
from google.cloud import tasks_v2beta3 as tasks

import requests


def send_task_to_http_queue(
    queue: tasks.Queue, body: str = "", token: str = "", headers: dict = {}
) -> int:
    """Send a task to an HTTP queue.
    Args:
        queue: The queue to send task to.
        body: The body of the task.
        auth_token: An authorization token for the queue.
        headers: Headers to set on the task.
    Returns:
        The matching queue, or None if it doesn't exist.
    """

    # Use application default credentials if not supplied in a header
    if token:
        headers["Authorization"] = f"Bearer {token}"

    endpoint = f"https://cloudtasks.googleapis.com/v2beta3/{queue.name}/tasks:buffer"
    response = requests.post(endpoint, body, headers=headers)

    return response.status_code


# [END cloud_tasks_send_task_to_http_queue]
