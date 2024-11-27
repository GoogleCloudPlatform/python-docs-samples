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

# [START dataplex_update_entry_type]
from google.cloud import dataplex_v1


def update_entry_type(
    project_id: str, location: str, entry_type_id: str
) -> dataplex_v1.EntryType:
    """Method to update Entry Type located in project_id, location and with entry_type_id"""

    # Initialize client that will be used to send requests across threads. This
    # client only needs to be created once, and can be reused for multiple requests.
    # After completing all of your requests, call the "__exit__()" method to safely
    # clean up any remaining background resources. Alternatively, use the client as
    # a context manager.
    with dataplex_v1.CatalogServiceClient() as client:
        # The resource name of the Entry Type
        name = f"projects/{project_id}/locations/{location}/entryTypes/{entry_type_id}"
        entry_type = dataplex_v1.EntryType(
            name=name, description="updated description of the entry type"
        )

        # Update mask specifies which fields will be updated.
        # For more information on update masks, see: https://google.aip.dev/161
        update_mask = {"paths": ["description"]}
        update_operation = client.update_entry_type(
            entry_type=entry_type, update_mask=update_mask
        )
        return update_operation.result(60)


if __name__ == "__main__":
    # TODO(developer): Replace these variables before running the sample.
    project_id = "MY_PROJECT_ID"
    # Available locations: https://cloud.google.com/dataplex/docs/locations
    location = "MY_LOCATION"
    entry_type_id = "MY_ENTRY_TYPE_ID"

    updated_entry_type = update_entry_type(project_id, location, entry_type_id)
    print(f"Successfully updated entry type: {updated_entry_type.name}")
# [END dataplex_update_entry_type]
