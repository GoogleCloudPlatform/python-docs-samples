# Copyright 2024 Google LLC
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

# [START dataplex_search_entries]
from typing import List

from google.cloud import dataplex_v1
from google.cloud.dataplex_v1 import Entry


def search_entries(project_id: str, query: str) -> List[Entry]:
    """Method to search Entries located in project_id and matching query"""

    # Initialize client that will be used to send requests across threads. This
    # client only needs to be created once, and can be reused for multiple requests.
    # After completing all of your requests, call the "__exit__()" method to safely
    # clean up any remaining background resources. Alternatively, use the client as
    # a context manager.
    with dataplex_v1.CatalogServiceClient() as client:
        search_entries_request = dataplex_v1.SearchEntriesRequest(
            page_size=100,
            # Required field, will by default limit search scope to organization under which the project is located
            name=f"projects/{project_id}/locations/global",
            # Optional field, will further limit search scope only to specified project
            scope=f"projects/{project_id}",
            query=query,
        )

        search_entries_response = client.search_entries(search_entries_request)
        return [
            result.dataplex_entry
            for result in search_entries_response._response.results
        ]


if __name__ == "__main__":
    # TODO(developer): Replace these variables before running the sample.
    project_id = "MY_PROJECT_ID"
    # How to write query for search: https://cloud.google.com/dataplex/docs/search-syntax
    query = "MY_QUERY"

    entries = search_entries(project_id, query)
    for entry in entries:
        print(f"Entry name found in search: {entry.name}")
# [END dataplex_search_entries]
