# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START job_search_list_tenants]

from google.cloud import talent
import six


def list_tenants(project_id):
    """List Tenants"""

    client = talent.TenantServiceClient()

    # project_id = 'Your Google Cloud Project ID'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    parent = f"projects/{project_id}"

    # Iterate over all results
    for response_item in client.list_tenants(parent=parent):
        print(f"Tenant Name: {response_item.name}")
        print(f"External ID: {response_item.external_id}")


# [END job_search_list_tenants]
