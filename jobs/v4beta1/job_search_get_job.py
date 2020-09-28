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

# [START job_search_get_job]

from google.cloud import talent
import six


def get_job(project_id, tenant_id, job_id):
    """Get Job"""

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # job_id = 'Job ID'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(job_id, six.binary_type):
        job_id = job_id.decode("utf-8")
    name = client.job_path(project_id, tenant_id, job_id)

    response = client.get_job(name)
    print("Job name: {}".format(response.name))
    print("Requisition ID: {}".format(response.requisition_id))
    print("Title: {}".format(response.title))
    print("Description: {}".format(response.description))
    print("Posting language: {}".format(response.language_code))
    for address in response.addresses:
        print("Address: {}".format(address))
    for email in response.application_info.emails:
        print("Email: {}".format(email))
    for website_uri in response.application_info.uris:
        print("Website: {}".format(website_uri))


# [END job_search_get_job]
