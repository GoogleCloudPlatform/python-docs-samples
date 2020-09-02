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
def list_queues(project, location):
    """List all task queues."""

    from google.cloud import tasks_v2

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Construct the fully qualified location path.
    parent = f"projects/{project}/locations/{location}"

    # Use the client to obtain the queues.
    response = client.list_queues(request={"parent": parent})

    # Print the results.
    num_results = 0
    for queue in response:
        num_results = num_results + 1
        print(queue.name)

    if num_results == 0:
        print("No queues found!")


# [END cloud_tasks_list_queues]
