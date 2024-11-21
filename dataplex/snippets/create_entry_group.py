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

# [START dataplex_create_entry_group]
from google.cloud import dataplex_v1


def create_entry_group(
    project_id: str, location: str, entry_group_id: str
) -> dataplex_v1.EntryGroup:
    """Method to create Entry Group located in project_id, location and with entry_group_id"""

    # Initialize client that will be used to send requests across threads. This
    # client only needs to be created once, and can be reused for multiple requests.
    # After completing all of your requests, call the "__exit__()" method to safely
    # clean up any remaining background resources. Alternatively, use the client as
    # a context manager.
    with dataplex_v1.CatalogServiceClient() as client:
        # The resource name of the Entry Group location
        parent = f"projects/{project_id}/locations/{location}"
        entry_group = dataplex_v1.EntryGroup(
            description="description of the entry group"
        )
        create_operation = client.create_entry_group(
            parent=parent, entry_group=entry_group, entry_group_id=entry_group_id
        )
        return create_operation.result(60)


if __name__ == "__main__":
    # TODO(developer): Replace these variables before running the sample.
    project_id = "MY_PROJECT_ID"
    # Available locations: https://cloud.google.com/dataplex/docs/locations
    location = "MY_LOCATION"
    entry_group_id = "MY_ENTRY_GROUP_ID"

    created_entry_group = create_entry_group(project_id, location, entry_group_id)
    print(f"Successfully created entry group: {created_entry_group.name}")
# [END dataplex_create_entry_group]
