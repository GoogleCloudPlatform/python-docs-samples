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

# [START job_search_histogram_search]
from google.cloud import talent


def search_jobs(project_id, tenant_id, query):
    """
    Search Jobs with histogram queries

    Args:
      query Histogram query
      More info on histogram facets, constants, and built-in functions:
      https://godoc.org/google.golang.org/genproto/googleapis/cloud/talent/v4beta1#SearchJobsRequest
    """

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # query = 'count(base_compensation, [bucket(12, 20)])'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(query, bytes):
        query = query.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    domain = "www.example.com"
    session_id = "Hashed session identifier"
    user_id = "Hashed user identifier"
    request_metadata = {"domain": domain, "session_id": session_id, "user_id": user_id}
    histogram_queries_element = {"histogram_query": query}
    histogram_queries = [histogram_queries_element]

    # Iterate over all results
    results = []
    request = talent.SearchJobsRequest(
        parent=parent,
        request_metadata=request_metadata,
        histogram_queries=histogram_queries,
    )
    for response_item in client.search_jobs(request=request).matching_jobs:
        print("Job summary: {response_item.job_summary}")
        print("Job title snippet: {response_item.job_title_snippet}")
        job = response_item.job
        results.append(job)
        print("Job name: {job.name}")
        print("Job title: {job.title}")
    return results


# [END job_search_histogram_search]
