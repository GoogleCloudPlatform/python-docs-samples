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

# [START dataplex_list_entries]
from typing import List

from google.cloud import dataplex_v1


def list_entries(
    project_id: str, location: str, entry_group_id: str
) -> List[dataplex_v1.Entry]:
    """Method to list Entries located in project_id, location and entry_group_id"""

    # Initialize client that will be used to send requests across threads. This
    # client only needs to be created once, and can be reused for multiple requests.
    # After completing all of your requests, call the "__exit__()" method to safely
    # clean up any remaining background resources. Alternatively, use the client as
    # a context manager.
    with dataplex_v1.CatalogServiceClient() as client:
        # The resource name of the Entries location
        parent = (
            f"projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}"
        )
        list_entries_request = dataplex_v1.ListEntriesRequest(
            parent=parent,
            # A filter on the entries to return. Filters are case-sensitive.
            # You can filter the request by the following fields:
            # * entry_type
            # * entry_source.display_name
            # To learn more about filters in general, see:
            # https://cloud.google.com/sdk/gcloud/reference/topic/filters
            filter="entry_type=projects/dataplex-types/locations/global/entryTypes/generic",
        )

        results = client.list_entries(request=list_entries_request)
        return list(results)


if __name__ == "__main__":
    # TODO(developer): Replace these variables before running the sample.
    project_id = "MY_PROJECT_ID"
    # Available locations: https://cloud.google.com/dataplex/docs/locations
    location = "MY_LOCATION"
    entry_group_id = "MY_ENTRY_GROUP_ID"

    entries = list_entries(project_id, location, entry_group_id)
    for entry in entries:
        print(f"Entry name: {entry.name}")
# [END dataplex_list_entries]
