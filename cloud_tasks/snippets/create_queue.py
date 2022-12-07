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
def create_queue(project, queue_name, location):
    """Create a task queue."""

    from google.cloud import tasks_v2

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Construct the fully qualified location path.
    parent = f"projects/{project}/locations/{location}"

    # Construct the create queue request.
    queue = {"name": client.queue_path(project, location, queue_name)}

    # Use the client to create the queue.
    response = client.create_queue(request={"parent": parent, "queue": queue})

    print("Created queue {}".format(response.name))
    return response


# [END cloud_tasks_create_queue]
