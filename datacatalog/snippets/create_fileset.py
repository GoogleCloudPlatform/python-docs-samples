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


def create_fileset(override_values):
    """Creates a fileset within an entry group."""
    # [START data_catalog_create_fileset]
    # Import required modules.
    from google.cloud import datacatalog_v1

    # TODO: Set these values before running the sample.
    project_id = "project_id"
    fileset_entry_group_id = "entry_group_id"
    fileset_entry_id = "entry_id"

    # [END data_catalog_create_fileset]

    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = override_values.get("project_id", project_id)
    fileset_entry_group_id = override_values.get(
        "fileset_entry_group_id", fileset_entry_group_id
    )
    fileset_entry_id = override_values.get("fileset_entry_id", fileset_entry_id)

    # [START data_catalog_create_fileset]
    # For all regions available, see:
    # https://cloud.google.com/data-catalog/docs/concepts/regions
    location = "us-central1"

    datacatalog = datacatalog_v1.DataCatalogClient()

    # Create an Entry Group.
    entry_group_obj = datacatalog_v1.types.EntryGroup()
    entry_group_obj.display_name = "My Fileset Entry Group"
    entry_group_obj.description = "This Entry Group consists of ...."

    entry_group = datacatalog.create_entry_group(
        parent=datacatalog_v1.DataCatalogClient.common_location_path(
            project_id, location
        ),
        entry_group_id=fileset_entry_group_id,
        entry_group=entry_group_obj,
    )
    print(f"Created entry group: {entry_group.name}")

    # Create a Fileset Entry.
    entry = datacatalog_v1.types.Entry()
    entry.display_name = "My Fileset"
    entry.description = "This fileset consists of ...."
    entry.gcs_fileset_spec.file_patterns.append("gs://my_bucket/*.csv")
    entry.type_ = datacatalog_v1.EntryType.FILESET

    # Create the Schema, for example when you have a csv file.
    entry.schema.columns.append(
        datacatalog_v1.types.ColumnSchema(
            column="first_name",
            description="First name",
            mode="REQUIRED",
            type_="STRING",
        )
    )

    entry.schema.columns.append(
        datacatalog_v1.types.ColumnSchema(
            column="last_name", description="Last name", mode="REQUIRED", type_="STRING"
        )
    )

    # Create the addresses parent column
    addresses_column = datacatalog_v1.types.ColumnSchema(
        column="addresses", description="Addresses", mode="REPEATED", type_="RECORD"
    )

    # Create sub columns for the addresses parent column
    addresses_column.subcolumns.append(
        datacatalog_v1.types.ColumnSchema(
            column="city", description="City", mode="NULLABLE", type_="STRING"
        )
    )

    addresses_column.subcolumns.append(
        datacatalog_v1.types.ColumnSchema(
            column="state", description="State", mode="NULLABLE", type_="STRING"
        )
    )

    entry.schema.columns.append(addresses_column)

    entry = datacatalog.create_entry(
        parent=entry_group.name, entry_id=fileset_entry_id, entry=entry
    )
    print(f"Created fileset entry: {entry.name}")
    # [END data_catalog_create_fileset]
