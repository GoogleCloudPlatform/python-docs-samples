# Copyright 2020 Google LLC
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

# [START cloud_tasks_delete_queue]
from google.cloud import tasks_v2


def delete_queue(project: str, location: str, queue_id: str) -> None:
    """Delete a queue.
    Args:
        project: The project ID where the queue is located.
        location: The location ID where the queue is located.
        queue_id: The ID of the queue to delete.
    """

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Use the client to send a DeleteQueueRequest.
    client.delete_queue(
        tasks_v2.DeleteQueueRequest(name=client.queue_path(project, location, queue_id))
    )


# [END cloud_tasks_delete_queue]
