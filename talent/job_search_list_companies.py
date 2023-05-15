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

# [START job_search_list_companies]

from google.cloud import talent


def list_companies(project_id, tenant_id):
    """List Companies"""

    client = talent.CompanyServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"

    # Iterate over all results
    results = []
    for company in client.list_companies(parent=parent):
        results.append(company.name)
        print(f"Company Name: {company.name}")
        print(f"Display Name: {company.display_name}")
        print(f"External ID: {company.external_id}")
    return results


# [END job_search_list_companies]
