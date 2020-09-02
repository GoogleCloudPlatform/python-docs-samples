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
def delete_queue(project, queue_name, location):
    """Delete a task queue."""

    from google.cloud import tasks_v2

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Get the fully qualified path to queue.
    queue = client.queue_path(project, location, queue_name)

    # Use the client to delete the queue.
    client.delete_queue(request={"name": queue})
    print("Deleted queue")


# [END cloud_tasks_delete_queue]
