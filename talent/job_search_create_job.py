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

# [START job_search_create_job]

from google.cloud import talent


def create_job(
    project_id,
    tenant_id,
    company_id,
    requisition_id,
    job_application_url,
):
    """Create Job"""

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # company_id = 'Company name, e.g. projects/your-project/companies/company-id'
    # requisition_id = 'Job requisition ID, aka Posting ID. Unique per job.'
    # title = 'Software Engineer'
    # description = 'This is a description of this <i>wonderful</i> job!'
    # job_application_url = 'https://www.example.org/job-posting/123'
    # address_one = '1600 Amphitheatre Parkway, Mountain View, CA 94043'
    # address_two = '111 8th Avenue, New York, NY 10011'
    # language_code = 'en-US'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(company_id, bytes):
        company_id = company_id.decode("utf-8")
    if isinstance(requisition_id, bytes):
        requisition_id = requisition_id.decode("utf-8")
    if isinstance(job_application_url, bytes):
        job_application_url = job_application_url.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    uris = [job_application_url]
    application_info = {"uris": uris}
    addresses = [
        "1600 Amphitheatre Parkway, Mountain View, CA 94043",
        "111 8th Avenue, New York, NY 10011",
    ]
    job = {
        "company": company_id,
        "requisition_id": requisition_id,
        "title": "Software Developer",
        "description": "Develop, maintain the software solutions.",
        "application_info": application_info,
        "addresses": addresses,
        "language_code": "en-US",
    }

    response = client.create_job(parent=parent, job=job)
    print(f"Created job: {response.name}")
    return response.name


# [END job_search_create_job]
