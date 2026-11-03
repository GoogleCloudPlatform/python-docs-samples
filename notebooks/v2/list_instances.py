# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START notebooks_v2_list_instances]
import sys

from google.api_core import exceptions
from google.cloud import notebooks_v2


def list_instances(
    project_id: str,
    location_id: str = "us-central1-a",
) -> None:
    """Lists Workbench instances in a zone.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone to list instances from.
    """
    client = notebooks_v2.NotebookServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    request = notebooks_v2.ListInstancesRequest(parent=parent)

    try:
        response = client.list_instances(request=request)
        for instance in response:
            print(f"Resource ID: {instance.name}")
            print(f"Creation Date: {instance.create_time}")
            print(f"Instance ID: {instance.id}")
            print(f"Proxy URI: {instance.proxy_uri}")
            print(f"State: {instance.state.name}")
    except exceptions.NotFound as err:
        print(
            f"error: Could not list instances in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_list_instances]
