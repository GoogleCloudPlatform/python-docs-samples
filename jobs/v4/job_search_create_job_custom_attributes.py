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

# [START job_search_create_job_custom_attributes]

from google.cloud import talent_v4beta1
import six


def sample_create_job(
    project_id, tenant_id, company_name, requisition_id, language_code
):
    """Create Job with Custom Attributes"""

    client = talent_v4beta1.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # company_name = 'Company name, e.g. projects/your-project/companies/company-id'
    # requisition_id = 'Job requisition ID, aka Posting ID. Unique per job.'
    # language_code = 'en-US'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(company_name, six.binary_type):
        company_name = company_name.decode("utf-8")
    if isinstance(requisition_id, six.binary_type):
        requisition_id = requisition_id.decode("utf-8")
    if isinstance(language_code, six.binary_type):
        language_code = language_code.decode("utf-8")
    parent = client.tenant_path(project_id, tenant_id)
    job = {
        "company": company_name,
        "requisition_id": requisition_id,
        "language_code": language_code,
    }

    response = client.create_job(parent, job)
    print("Created job: {}".format(response.name))


# [END job_search_create_job_custom_attributes]
