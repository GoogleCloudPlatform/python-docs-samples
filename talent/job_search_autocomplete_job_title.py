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

# [START job_search_autocomplete_job_title]
from google.cloud import talent_v4beta1


def complete_query(project_id, tenant_id, query):
    """Complete job title given partial text (autocomplete)"""

    client = talent_v4beta1.CompletionClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # query = '[partially typed job title]'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(query, bytes):
        query = query.decode("utf-8")

    parent = f"projects/{project_id}/tenants/{tenant_id}"

    request = talent_v4beta1.CompleteQueryRequest(
        parent=parent,
        query=query,
        page_size=5,  # limit for number of results
        language_codes=["en-US"],  # language code
    )
    response = client.complete_query(request=request)
    for result in response.completion_results:
        print(f"Suggested title: {result.suggestion}")
        # Suggestion type is JOB_TITLE or COMPANY_TITLE
        print(
            f"Suggestion type: {talent_v4beta1.CompleteQueryRequest.CompletionType(result.type_).name}"
        )


# [END job_search_autocomplete_job_title]
