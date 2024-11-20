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

# [START dataplex_get_entry]
from google.cloud import dataplex_v1


def get_entry(
    project_id: str, location: str, entry_group_id: str, entry_id: str
) -> dataplex_v1.Entry:
    """Method to retrieve Entry located in project_id, location, entry_group_id and with entry_id

    When Entry is created in Dataplex for example for BigQuery table,
    access permissions might differ between Dataplex and source system.
    "Get" method checks permissions in Dataplex.
    Please also refer how to lookup an Entry, which checks permissions in source system.
    """

    # Initialize client that will be used to send requests across threads. This
    # client only needs to be created once, and can be reused for multiple requests.
    # After completing all of your requests, call the "__exit__()" method to safely
    # clean up any remaining background resources. Alternatively, use the client as
    # a context manager.
    with dataplex_v1.CatalogServiceClient() as client:
        # The resource name of the Entry
        name = f"projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}/entries/{entry_id}"
        get_entry_request = dataplex_v1.GetEntryRequest(
            name=name,
            # View determines which Aspects are returned with the Entry.
            # For all available options, see:
            # https://cloud.google.com/sdk/gcloud/reference/dataplex/entries/lookup#--view
            view=dataplex_v1.EntryView.FULL,
            # Following 2 lines will be ignored, because "View" is set to FULL.
            # Their purpose is to demonstrate how to filter the Aspects returned for Entry
            # when "View" is set to CUSTOM.
            aspect_types=[
                "projects/dataplex-types/locations/global/aspectTypes/generic"
            ],
            paths=["my_path"],
        )
        return client.get_entry(request=get_entry_request)


if __name__ == "__main__":
    # TODO(developer): Replace these variables before running the sample.
    project_id = "MY_PROJECT_ID"
    # Available locations: https://cloud.google.com/dataplex/docs/locations
    location = "MY_LOCATION"
    entry_group_id = "MY_ENTRY_GROUP_ID"
    entry_id = "MY_ENTRY_ID"

    entry = get_entry(project_id, location, entry_group_id, entry_id)
    print(f"Entry retrieved successfully: {entry.name}")
    for aspect_key in entry.aspects.keys():
        print(f"Retrieved aspect for entry: {aspect_key}")
# [END dataplex_get_entry]
