# Copyright 2022 Google LLC
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
#

# [START enterpriseknowledgegraph_lookup]

from typing import Sequence

from google.cloud import enterpriseknowledgegraph as ekg

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_GRAPH_LOCATION'      # Values: 'global'
# ids = ['YOUR_LOOKUP_MID']             # https://cloud.google.com/enterprise-knowledge-graph/docs/mid
# languages = ['en']                    # Optional: List of ISO 639-1 Codes


def lookup_sample(
    project_id: str,
    location: str,
    ids: Sequence[str],
    languages: Sequence[str] = None,
):
    # Create a client
    client = ekg.EnterpriseKnowledgeGraphServiceClient()

    # The full resource name of the location
    # e.g. projects/{project_id}/locations/{location}
    parent = client.common_location_path(project=project_id, location=location)

    # Initialize request argument(s)
    request = ekg.LookupRequest(
        parent=parent,
        ids=ids,
        languages=languages,
    )

    # Make the request
    response = client.lookup(request=request)

    print(f"Lookup IDs: {ids}\n")

    print(response)

    # Extract and print date from response
    for item in response.item_list_element:
        result = item.get("result")

        print(f"Name: {result.get('name')}")
        print(f"- Description: {result.get('description')}")
        print(f"- Types: {result.get('@type')}\n")

        detailed_description = result.get("detailedDescription")

        if detailed_description:
            print("- Detailed Description:")
            print(f"\t- Article Body: {detailed_description.get('articleBody')}")
            print(f"\t- URL: {detailed_description.get('url')}")
            print(f"\t- License: {detailed_description.get('license')}\n")

        print(f"- Cloud MID: {result.get('@id')}")
        for identifier in result.get("identifier"):
            print(f"\t- {identifier.get('name')}: {identifier.get('value')}")

        print("\n")


# [END enterpriseknowledgegraph_lookup]
