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

# [START cloud_tasks_list_queues]
from typing import List

from google.cloud import tasks_v2


def list_queues(project: str, location: str) -> List[str]:
    """List all queues
    Args:
        project: The project ID to list queues from.
        location: The location ID to list queues from.

    Returns:
        A list of queue names.
    """

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Use the client to send a ListQueuesRequest.
    response = client.list_queues(
        tasks_v2.ListQueuesRequest(
            parent=client.common_location_path(project, location)
        )
    )

    # Return the results.
    return [queue.name for queue in response]


# [END cloud_tasks_list_queues]
