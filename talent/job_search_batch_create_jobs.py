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

# [START job_search_batch_create_jobs]

from google.cloud import talent
import six


def batch_create_jobs(
    project_id,
    tenant_id,
    company_name_one,
    requisition_id_one,
    title_one,
    description_one,
    job_application_url_one,
    address_one,
    language_code_one,
    company_name_two,
    requisition_id_two,
    title_two,
    description_two,
    job_application_url_two,
    address_two,
    language_code_two,
):
    """
    Batch Create Jobs

    Args:
      project_id Your Google Cloud Project ID
      tenant_id Identifier of the Tenant
    """

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # company_name_one = 'Company name, e.g. projects/your-project/companies/company-id'
    # requisition_id_one = 'Job requisition ID, aka Posting ID. Unique per job.'
    # title_one = 'Software Engineer'
    # description_one = 'This is a description of this <i>wonderful</i> job!'
    # job_application_url_one = 'https://www.example.org/job-posting/123'
    # address_one = '1600 Amphitheatre Parkway, Mountain View, CA 94043'
    # language_code_one = 'en-US'
    # company_name_two = 'Company name, e.g. projects/your-project/companies/company-id'
    # requisition_id_two = 'Job requisition ID, aka Posting ID. Unique per job.'
    # title_two = 'Quality Assurance'
    # description_two = 'This is a description of this <i>wonderful</i> job!'
    # job_application_url_two = 'https://www.example.org/job-posting/123'
    # address_two = '111 8th Avenue, New York, NY 10011'
    # language_code_two = 'en-US'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(company_name_one, bytes):
        company_name_one = company_name_one.decode("utf-8")
    if isinstance(requisition_id_one, bytes):
        requisition_id_one = requisition_id_one.decode("utf-8")
    if isinstance(title_one, bytes):
        title_one = title_one.decode("utf-8")
    if isinstance(description_one, bytes):
        description_one = description_one.decode("utf-8")
    if isinstance(job_application_url_one, bytes):
        job_application_url_one = job_application_url_one.decode("utf-8")
    if isinstance(address_one, bytes):
        address_one = address_one.decode("utf-8")
    if isinstance(language_code_one, bytes):
        language_code_one = language_code_one.decode("utf-8")
    if isinstance(company_name_two, bytes):
        company_name_two = company_name_two.decode("utf-8")
    if isinstance(requisition_id_two, bytes):
        requisition_id_two = requisition_id_two.decode("utf-8")
    if isinstance(title_two, bytes):
        title_two = title_two.decode("utf-8")
    if isinstance(description_two, bytes):
        description_two = description_two.decode("utf-8")
    if isinstance(job_application_url_two, bytes):
        job_application_url_two = job_application_url_two.decode("utf-8")
    if isinstance(address_two, bytes):
        address_two = address_two.decode("utf-8")
    if isinstance(language_code_two, bytes):
        language_code_two = language_code_two.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    uris = [job_application_url_one]
    application_info = {"uris": uris}
    addresses = [address_one]
    jobs_element = {
        "company": company_name_one,
        "requisition_id": requisition_id_one,
        "title": title_one,
        "description": description_one,
        "application_info": application_info,
        "addresses": addresses,
        "language_code": language_code_one,
    }
    uris_2 = [job_application_url_two]
    application_info_2 = {"uris": uris_2}
    addresses_2 = [address_two]
    jobs_element_2 = {
        "company": company_name_two,
        "requisition_id": requisition_id_two,
        "title": title_two,
        "description": description_two,
        "application_info": application_info_2,
        "addresses": addresses_2,
        "language_code": language_code_two,
    }
    jobs = [jobs_element, jobs_element_2]

    operation = client.batch_create_jobs(parent=parent, jobs=jobs)

    print("Waiting for operation to complete...")
    response = operation.result(90)

    print(f"Batch response: {response}")


# [END job_search_batch_create_jobs]
