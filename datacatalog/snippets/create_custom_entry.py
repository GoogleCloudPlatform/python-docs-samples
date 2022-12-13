# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def create_custom_entry(override_values):
    """Creates a custom entry within an entry group."""
    # [START data_catalog_create_custom_entry]
    # Import required modules.
    from google.cloud import datacatalog_v1

    # Google Cloud Platform project.
    project_id = "my-project"
    # Entry Group to be created.
    entry_group_id = "my_new_entry_group_id"
    # Entry to be created.
    entry_id = "my_new_entry_id"
    # Currently, Data Catalog stores metadata in the us-central1 region.
    location = "us-central1"

    # [END data_catalog_create_custom_entry]

    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = override_values.get("project_id", project_id)
    entry_id = override_values.get("entry_id", entry_id)
    entry_group_id = override_values.get("entry_group_id", entry_group_id)

    # [START data_catalog_create_custom_entry]
    datacatalog = datacatalog_v1.DataCatalogClient()

    # Create an Entry Group.
    entry_group_obj = datacatalog_v1.types.EntryGroup()
    entry_group_obj.display_name = "My awesome Entry Group"
    entry_group_obj.description = "This Entry Group represents an external system"

    entry_group = datacatalog.create_entry_group(
        parent=datacatalog_v1.DataCatalogClient.common_location_path(
            project_id, location
        ),
        entry_group_id=entry_group_id,
        entry_group=entry_group_obj,
    )
    entry_group_name = entry_group.name
    print("Created entry group: {}".format(entry_group_name))

    # Create an Entry.
    entry = datacatalog_v1.types.Entry()
    entry.user_specified_system = "onprem_data_system"
    entry.user_specified_type = "onprem_data_asset"
    entry.display_name = "My awesome data asset"
    entry.description = "This data asset is managed by an external system."
    entry.linked_resource = "//my-onprem-server.com/dataAssets/my-awesome-data-asset"

    # Create the Schema, this is optional.
    entry.schema.columns.append(
        datacatalog_v1.types.ColumnSchema(
            column="first_column",
            type_="STRING",
            description="This columns consists of ....",
            mode=None,
        )
    )

    entry.schema.columns.append(
        datacatalog_v1.types.ColumnSchema(
            column="second_column",
            type_="DOUBLE",
            description="This columns consists of ....",
            mode=None,
        )
    )

    entry = datacatalog.create_entry(
        parent=entry_group_name, entry_id=entry_id, entry=entry
    )
    print("Created entry: {}".format(entry.name))
    # [END data_catalog_create_custom_entry]
