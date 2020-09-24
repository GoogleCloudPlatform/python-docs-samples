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

# [START job_search_get_company]

from google.cloud import talent
import six


def get_company(project_id, tenant_id, company_id):
    """Get Company"""

    client = talent.CompanyServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # company_id = 'Company ID'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(company_id, six.binary_type):
        company_id = company_id.decode("utf-8")
    name = client.company_path(project_id, tenant_id, company_id)

    response = client.get_company(name=name)
    print(f"Company name: {response.name}")
    print(f"Display name: {response.display_name}")


# [END job_search_get_company]
