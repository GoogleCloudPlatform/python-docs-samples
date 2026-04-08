# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START retail_v2_search_pagination]
import sys

from google.api_core import exceptions
from google.cloud import retail_v2

client = retail_v2.SearchServiceClient()


def search_pagination(
    project_id: str,
    placement_id: str,
    visitor_id: str,
    query: str,
) -> None:
    """Search for products with pagination using Vertex AI Search for commerce.

    Performs a search request, then uses the next_page_token to get the next page.

    Args:
        project_id: The Google Cloud project ID.
        placement_id: The placement name for the search.
        visitor_id: A unique identifier for the user.
        query: The search term.
    """
    placement_path = client.serving_config_path(
        project=project_id,
        location="global",
        catalog="default_catalog",
        serving_config=placement_id,
    )

    branch_path = client.branch_path(
        project=project_id,
        location="global",
        catalog="default_catalog",
        branch="default_branch",
    )

    # First page request
    first_request = retail_v2.SearchRequest(
        placement=placement_path,
        branch=branch_path,
        visitor_id=visitor_id,
        query=query,
        page_size=5,
    )

    try:
        first_response = client.search(request=first_request)
        print("--- First Page ---")
        first_page = next(first_response.pages)
        for result in first_page.results:
            print(f"Product ID: {result.product.id}")

        next_page_token = first_response.next_page_token

        if next_page_token:
            # Second page request using page_token
            second_request = retail_v2.SearchRequest(
                placement=placement_path,
                branch=branch_path,
                visitor_id=visitor_id,
                query=query,
                page_size=5,
                page_token=next_page_token,
            )
            second_response = client.search(request=second_request)
            print("\n--- Second Page ---")
            second_page = next(second_response.pages)
            for result in second_page.results:
                print(f"Product ID: {result.product.id}")
        else:
            print("\nNo more pages.")

    except exceptions.GoogleAPICallError as e:
        print(f"error: {e.message}", file=sys.stderr)


# [END retail_v2_search_pagination]
