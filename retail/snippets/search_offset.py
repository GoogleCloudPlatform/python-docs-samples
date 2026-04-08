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

# [START retail_v2_search_offset]
import sys

from google.api_core import exceptions
from google.cloud import retail_v2

client = retail_v2.SearchServiceClient()


def search_offset(
    project_id: str,
    placement_id: str,
    visitor_id: str,
    query: str,
    offset: int,
) -> None:
    """Search for products with an offset using Vertex AI Search for commerce.

    Performs a search request starting from a specified position.

    Args:
        project_id: The Google Cloud project ID.
        placement_id: The placement name for the search.
        visitor_id: A unique identifier for the user.
        query: The search term.
        offset: The number of results to skip.
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

    request = retail_v2.SearchRequest(
        placement=placement_path,
        branch=branch_path,
        visitor_id=visitor_id,
        query=query,
        page_size=10,
        offset=offset,
    )

    try:
        response = client.search(request=request)

        print(f"--- Results for offset: {offset} ---")
        for result in response:
            product = result.product
            print(f"Product ID: {product.id}")
            print(f"  Title: {product.title}")
            print(f"  Scores: {result.model_scores}")

    except exceptions.GoogleAPICallError as e:
        print(f"error: {e.message}", file=sys.stderr)


# [END retail_v2_search_offset]
