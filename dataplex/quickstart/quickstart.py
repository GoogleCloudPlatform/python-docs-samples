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
# [START dataplex_quickstart]
import time

from google.cloud import dataplex_v1
from google.protobuf import struct_pb2


# Method to demonstrate lifecycle of different Dataplex resources and their interactions.
# Method creates Aspect Type, Entry Type, Entry Group and Entry, retrieves Entry
# and cleans up created resources.
def quickstart(
    project_id: str,
    location: str,
    aspect_type_id: str,
    entry_type_id: str,
    entry_group_id: str,
    entry_id: str,
) -> None:
    # Initialize client that will be used to send requests across threads. This
    # client only needs to be created once, and can be reused for multiple requests.
    # After completing all of your requests, call the "__exit__()" method to safely
    # clean up any remaining background resources. Alternatively, use the client as
    # a context manager.
    with dataplex_v1.CatalogServiceClient() as client:
        # 0) Prepare variables used in following steps
        global_parent = f"projects/{project_id}/locations/global"
        specific_location_parent = f"projects/{project_id}/locations/{location}"

        # 1) Create Aspect Type that will be attached to Entry Type
        aspect_field = dataplex_v1.AspectType.MetadataTemplate(
            # The name must follow regex ^(([a-zA-Z]{1})([\\w\\-_]{0,62}))$
            # That means name must only contain alphanumeric character or dashes or underscores,
            # start with an alphabet, and must be less than 63 characters.
            name="example_field",
            # Metadata Template is recursive structure,
            # primitive types such as "string" or "integer" indicate leaf node,
            # complex types such as "record" or "array" would require nested Metadata Template
            type="string",
            index=1,
            annotations=dataplex_v1.AspectType.MetadataTemplate.Annotations(
                description="example field to be filled during entry creation"
            ),
            constraints=dataplex_v1.AspectType.MetadataTemplate.Constraints(
                # Specifies if field will be required in Aspect Type.
                required=True
            ),
        )
        aspect_type = dataplex_v1.AspectType(
            description="aspect type for dataplex quickstart",
            metadata_template=dataplex_v1.AspectType.MetadataTemplate(
                name="example_template",
                type="record",
                # Aspect Type fields, that themselves are Metadata Templates.
                record_fields=[aspect_field],
            ),
        )
        aspect_type_create_operation = client.create_aspect_type(
            # Aspect Type is created in "global" location to highlight, that resources from
            # "global" region can be attached to Entry created in specific location
            parent=global_parent,
            aspect_type=aspect_type,
            aspect_type_id=aspect_type_id,
        )
        created_aspect_type = aspect_type_create_operation.result(60)
        print(f"Step 1: Created aspect type -> {created_aspect_type.name}")

        # 2) Create Entry Type, of which type Entry will be created
        entry_type = dataplex_v1.EntryType(
            description="entry type for dataplex quickstart",
            required_aspects=[
                dataplex_v1.EntryType.AspectInfo(
                    # Aspect Type created in step 1
                    type=f"projects/{project_id}/locations/global/aspectTypes/{aspect_type_id}"
                )
            ],
        )
        entry_type_create_operation = client.create_entry_type(
            # Entry Type is created in "global" location to highlight, that resources from
            # "global" region can be attached to Entry created in specific location
            parent=global_parent,
            entry_type=entry_type,
            entry_type_id=entry_type_id,
        )
        created_entry_type = entry_type_create_operation.result(60)
        print(f"Step 2: Created entry type -> {created_entry_type.name}")

        # 3) Create Entry Group in which Entry will be located
        entry_group = dataplex_v1.EntryGroup(
            description="entry group for dataplex quickstart"
        )
        entry_group_create_operation = client.create_entry_group(
            # Entry Group is created for specific location
            parent=specific_location_parent,
            entry_group=entry_group,
            entry_group_id=entry_group_id,
        )
        created_entry_group = entry_group_create_operation.result(60)
        print(f"Step 3: Created entry group -> {created_entry_group.name}")

        # 4) Create Entry
        # Wait 10 second to allow previously created resources to propagate
        time.sleep(10)
        aspect_key = f"{project_id}.global.{aspect_type_id}"
        entry = dataplex_v1.Entry(
            # Entry is an instance of Entry Type created in step 2
            entry_type=f"projects/{project_id}/locations/global/entryTypes/{entry_type_id}",
            entry_source=dataplex_v1.EntrySource(
                description="entry for dataplex quickstart"
            ),
            aspects={
                # Attach Aspect that is an instance of Aspect Type created in step 1
                aspect_key: dataplex_v1.Aspect(
                    aspect_type=f"projects/{project_id}/locations/global/aspectTypes/{aspect_type_id}",
                    data=struct_pb2.Struct(
                        fields={
                            "example_field": struct_pb2.Value(
                                string_value="example value for the field"
                            ),
                        }
                    ),
                )
            },
        )
        created_entry = client.create_entry(
            # Entry is created in specific location, but it is still possible to link it with
            # resources (Aspect Type and Entry Type) from "global" location
            parent=f"projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}",
            entry=entry,
            entry_id=entry_id,
        )
        print(f"Step 4: Created entry -> {created_entry.name}")

        # 5) Retrieve created Entry
        get_entry_request = dataplex_v1.GetEntryRequest(
            name=f"projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}/entries/{entry_id}",
            view=dataplex_v1.EntryView.FULL,
        )
        retrieved_entry = client.get_entry(request=get_entry_request)
        print(f"Step 5: Retrieved entry -> {retrieved_entry.name}")
        for retrieved_aspect in retrieved_entry.aspects.values():
            print("Retrieved aspect for entry:")
            print(f" * aspect type -> {retrieved_aspect.aspect_type}")
            print(f" * aspect field value -> {retrieved_aspect.data['example_field']}")

        # 6) Use Search capabilities to find Entry
        # Wait 30 second to allow resources to propagate to Search
        print("Step 6: Waiting for resources to propagate to Search...")
        time.sleep(30)
        search_entries_request = dataplex_v1.SearchEntriesRequest(
            name=global_parent, query="name:dataplex-quickstart-entry"
        )
        results = client.search_entries(search_entries_request)
        search_entries_response = results._response
        entries_from_search = [
            result.dataplex_entry for result in search_entries_response.results
        ]
        print("Entries found in Search:")
        # Please note in output that Entry Group and Entry Type are also represented as Entries
        for entry_from_search in entries_from_search:
            print(f" * {entry_from_search.name}")

        # 7) Clean created resources
        client.delete_entry_group(
            name=f"projects/{project_id}/locations/{location}/entryGroups/{entry_group_id}"
        )
        client.delete_entry_type(
            name=f"projects/{project_id}/locations/global/entryTypes/{entry_type_id}"
        )
        client.delete_aspect_type(
            name=f"projects/{project_id}/locations/global/aspectTypes/{aspect_type_id}"
        )
        print("Step 7: Successfully cleaned up resources")


if __name__ == "__main__":
    # TODO(developer): Replace these variables before running the sample.
    project_id = "MY_PROJECT_ID"
    # Available locations: https://cloud.google.com/dataplex/docs/locations
    location = "MY_LOCATION"
    # Variables below can be replaced with custom values or defaults can be kept
    aspect_type_id = "dataplex-quickstart-aspect-type"
    entry_type_id = "dataplex-quickstart-entry-type"
    entry_group_id = "dataplex-quickstart-entry-group"
    entry_id = "dataplex-quickstart-entry"

    quickstart(
        project_id, location, aspect_type_id, entry_type_id, entry_group_id, entry_id
    )
# [END dataplex_quickstart]
