# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import retail_v2

def search_products(project_id, catalog_id, placement_id, branch, visitor_id, query):
    client = retail_v2.SearchServiceClient()

    placement_name = retail_v2.SearchServiceClient.placement_path(
        project_id, location='global', catalog=catalog_id, placement=placement_id
    )

    search_request = retail_v2.SearchRequest(
        placement=placement_name,
        branch=branch,
        visitor_id=visitor_id,
        query=query,
        page_size=10
    )

    response = client.search(search_request)

    print(f"Search response: {response}")

    return response

# Example usage
project_id = 'YOUR_PROJECT_ID'
catalog_id = 'YOUR_CATALOG_ID'
placement_id = 'YOUR_PLACEMENT_ID'
branch = 'YOUR_BRANCH_NAME'
visitor_id = 'YOUR_VISITOR_ID'
query = 'YOUR_QUERY'

search_products(project_id, catalog_id, placement_id, branch, visitor_id, query)
