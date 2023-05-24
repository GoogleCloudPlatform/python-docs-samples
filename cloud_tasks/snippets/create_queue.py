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

# [START cloud_tasks_create_queue]
from google.cloud import tasks_v2


def create_queue(project: str, location: str, queue_id: str) -> tasks_v2.Queue:
    """Create a queue.
    Args:
        project: The project ID to create the queue in.
        location: The location to create the queue in.
        queue_id: The ID to use for the new queue.

    Returns:
        The newly created queue.
    """

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Use the client to send a CreateQueueRequest.
    return client.create_queue(
        tasks_v2.CreateQueueRequest(
            parent=client.common_location_path(project, location),
            queue=tasks_v2.Queue(name=client.queue_path(project, location, queue_id)),
        )
    )


# [END cloud_tasks_create_queue]
