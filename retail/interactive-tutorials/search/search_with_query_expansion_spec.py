# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Call Retail API to search for a products in a catalog,
# enabling the query expansion feature to let the Google Retail Search build an automatic query expansion.
#
# [START retail_search_for_products_with_query_expansion_specification]
import google.auth
from google.cloud.retail import SearchRequest, SearchServiceClient

project_id = google.auth.default()[1]


# get search service request:
def get_search_request(
    query: str, condition: SearchRequest.QueryExpansionSpec.Condition
):
    default_search_placement = (
        "projects/"
        + project_id
        + "/locations/global/catalogs/default_catalog/placements/default_search"
    )

    query_expansion_spec = SearchRequest().QueryExpansionSpec()
    query_expansion_spec.condition = condition

    search_request = SearchRequest()
    search_request.placement = default_search_placement  # Placement is used to identify the Serving Config name.
    search_request.query = query
    search_request.visitor_id = "123456"  # A unique identifier to track visitors
    search_request.query_expansion_spec = query_expansion_spec
    search_request.page_size = 10

    print("---search request:---")
    print(search_request)

    return search_request


# call the Retail Search:
def search():
    # TRY DIFFERENT QUERY EXPANSION CONDITION HERE:
    condition = SearchRequest.QueryExpansionSpec.Condition.AUTO

    search_request = get_search_request("Google Youth Hero Tee Grey", condition)
    search_response = SearchServiceClient().search(search_request)

    print("---search response---")
    if not search_response.results:
        print("The search operation returned no matching results.")
    else:
        print(search_response)
    return search_response
# [END retail_search_for_products_with_query_expansion_specification]


search()
