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
from google.cloud import talent


def create_job(project_id, tenant_id, company_id, requisition_id):
    """Create Job with Custom Attributes"""

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # company_id = 'Company name, e.g. projects/your-project/companies/company-id'
    # requisition_id = 'Job requisition ID, aka Posting ID. Unique per job.'
    # language_code = 'en-US'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(company_id, bytes):
        company_id = company_id.decode("utf-8")

    # Custom attribute can be string or numeric value,
    # and can be filtered in search queries.
    # https://cloud.google.com/talent-solution/job-search/docs/custom-attributes
    custom_attribute = talent.CustomAttribute()
    custom_attribute.filterable = True
    custom_attribute.string_values.append("Intern")
    custom_attribute.string_values.append("Apprenticeship")

    parent = f"projects/{project_id}/tenants/{tenant_id}"

    job = talent.Job(
        company=company_id,
        title="Software Engineer",
        requisition_id=requisition_id,
        description="This is a description of this job",
        language_code="en-us",
        custom_attributes={"FOR_STUDENTS": custom_attribute},
    )

    response = client.create_job(parent=parent, job=job)
    print(f"Created job: {response.name}")
    return response.name


# [END job_search_create_job_custom_attributes]
