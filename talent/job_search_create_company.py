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

# [START job_search_create_company]

from google.cloud import talent
import six


def create_company(project_id, tenant_id, display_name, external_id):
    """Create Company"""

    client = talent.CompanyServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # display_name = 'My Company Name'
    # external_id = 'Identifier of this company in my system'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(display_name, six.binary_type):
        display_name = display_name.decode("utf-8")
    if isinstance(external_id, six.binary_type):
        external_id = external_id.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    company = {"display_name": display_name, "external_id": external_id}

    response = client.create_company(parent=parent, company=company)
    print("Created Company")
    print("Name: {}".format(response.name))
    print("Display Name: {}".format(response.display_name))
    print("External ID: {}".format(response.external_id))
    return response.name


# [END job_search_create_company]
