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

# [START dataplex_create_entry]
from google.cloud import dataplex_v1
from google.protobuf import struct_pb2


def create_entry(
    project_id: str, location: str, entry_group_id: str, entry_id: str
) -> dataplex_v1.Entry:
    """Method to create Entry located in project_id, location, entry_group_id and with entry_id"""

    # Initialize client that will be used to send requests across threads. This
    # client only needs to be created once, and can be reused for multiple requests.
    # After completing all of your requests, call the "__exit__()" method to safely
    # clean up any remaining background resources. Alternatively, use the client as
    # a context manager.
    with dataplex_v1.CatalogServiceClient() as client:
        # The resource name of the Entry Group
        parent = (
            f"projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}"
        )
        entry = dataplex_v1.Entry(
            # Example of system Entry Type.
            # It is also possible to specify custom Entry Type.
            entry_type="projects/dataplex-types/locations/global/entryTypes/generic",
            entry_source=dataplex_v1.EntrySource(
                description="description of the entry"
            ),
            aspects={
                "dataplex-types.global.generic": dataplex_v1.Aspect(
                    # This is required Aspect Type for "generic" Entry Type.
                    # For custom Aspect Type required Entry Type would be different.
                    aspect_type="projects/dataplex-types/locations/global/aspectTypes/generic",
                    data=struct_pb2.Struct(
                        fields={
                            # "Generic" Aspect Type have fields called "type" and "system.
                            # The values below are a sample of possible options.
                            "type": struct_pb2.Value(string_value="example value"),
                            "system": struct_pb2.Value(string_value="example system"),
                        }
                    ),
                )
            },
        )
        return client.create_entry(parent=parent, entry=entry, entry_id=entry_id)


if __name__ == "__main__":
    # TODO(developer): Replace these variables before running the sample.
    project_id = "MY_PROJECT_ID"
    # Available locations: https://cloud.google.com/dataplex/docs/locations
    location = "MY_LOCATION"
    entry_group_id = "MY_ENTRY_GROUP_ID"
    entry_id = "MY_ENTRY_ID"

    created_entry = create_entry(project_id, location, entry_group_id, entry_id)
    print(f"Successfully created entry: {created_entry.name}")
# [END dataplex_create_entry]
