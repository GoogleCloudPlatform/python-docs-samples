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

# [START job_search_custom_ranking_search]

from google.cloud import talent
import six


def search_jobs(project_id, tenant_id):
    """Search Jobs using custom rankings"""

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    domain = "www.example.com"
    session_id = "Hashed session identifier"
    user_id = "Hashed user identifier"
    request_metadata = talent.RequestMetadata(
        domain=domain, session_id=session_id, user_id=user_id
    )
    importance_level = (
        talent.SearchJobsRequest.CustomRankingInfo.ImportanceLevel.EXTREME
    )
    ranking_expression = "(someFieldLong + 25) * 0.25"
    custom_ranking_info = {
        "importance_level": importance_level,
        "ranking_expression": ranking_expression,
    }
    order_by = "custom_ranking desc"

    # Iterate over all results
    results = []
    request = talent.SearchJobsRequest(
        parent=parent,
        request_metadata=request_metadata,
        custom_ranking_info=custom_ranking_info,
        order_by=order_by,
    )
    for response_item in client.search_jobs(request=request).matching_jobs:
        print(f"Job summary: {response_item.job_summary}")
        print(f"Job title snippet: {response_item.job_title_snippet}")
        job = response_item.job
        results.append(job.name)
        print(f"Job name: {job.name}")
        print(f"Job title: {job.title}")
    return results


# [END job_search_custom_ranking_search]
