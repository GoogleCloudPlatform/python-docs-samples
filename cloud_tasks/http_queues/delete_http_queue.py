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


# [START cloud_tasks_delete_http_queue]
# HTTP Queues are currently in public beta
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
