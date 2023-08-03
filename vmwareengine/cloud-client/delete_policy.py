# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START vmwareengine_delete_policy]
from google.api_core import operation
from google.cloud import vmwareengine_v1


def delete_network_policy(project_id: str, region: str) -> operation.Operation:
    """
    Delete a Network Policy.

    Args:
        project_id: name of the project hosting the policy.
        region: name of the region hosting the policy. I.e. "us-central1"

    Return:
        Operation object. You can use .result() to wait for it to finish.
    """
    client = vmwareengine_v1.VmwareEngineClient()
    return client.delete_network_policy(
        name=f"projects/{project_id}/locations/{region}/networkPolicies/{region}-default"
    )


# [END vmwareengine_delete_policy]
