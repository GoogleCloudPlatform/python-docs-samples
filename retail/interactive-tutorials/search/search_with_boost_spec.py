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

# Call Retail API to search for a products in a catalog, rerank the
# results boosting or burying the products that match defined condition.
#

import google.auth
from google.cloud.retail import SearchRequest, SearchServiceClient

project_id = google.auth.default()[1]


# get search service request:
def get_search_request(query: str, condition: str, boost_strength: float):
    default_search_placement = (
        "projects/"
        + project_id
        + "/locations/global/catalogs/default_catalog/placements/default_search"
    )

    condition_boost_spec = SearchRequest.BoostSpec.ConditionBoostSpec()
    condition_boost_spec.condition = condition
    condition_boost_spec.boost = boost_strength

    boost_spec = SearchRequest.BoostSpec()
    boost_spec.condition_boost_specs = [condition_boost_spec]

    search_request = SearchRequest()
    search_request.placement = default_search_placement  # Placement is used to identify the Serving Config name.
    search_request.query = query
    search_request.visitor_id = "123456"  # A unique identifier to track visitors
    search_request.boost_spec = boost_spec
    search_request.page_size = 10

    print("---search request---")
    print(search_request)

    return search_request


# call the Retail Search:
def search():
    # TRY DIFFERENT CONDITIONS HERE:
    condition = '(colorFamilies: ANY("Blue"))'
    boost = 0.0

    search_request = get_search_request("Tee", condition, boost)
    search_response = SearchServiceClient().search(search_request)
    print("---search response---")
    if not search_response.results:
        print("The search operation returned no matching results.")
    else:
        print(search_response)
    return search_response


search()
