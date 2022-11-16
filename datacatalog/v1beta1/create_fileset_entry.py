# Copyright 2019 Google LLC
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


def create_fileset_entry(client, entry_group_name, entry_id):
    # [START data_catalog_create_fileset_v1beta1]
    from google.cloud import datacatalog_v1beta1

    # TODO(developer): Construct a Data Catalog client object.
    # client = datacatalog_v1beta1.DataCatalogClient()
    # TODO(developer): Set entry_group_name to the Name of the entry group
    #  the entry will belong.
    # entry_group_name = "your_entry_group_name"
    # TODO(developer): Set entry_id to the ID of the entry to create.
    # entry_id = "your_entry_id"
    # Construct a full Entry object to send to the API.
    entry = datacatalog_v1beta1.types.Entry()
    entry.display_name = "My Fileset"
    entry.description = "This Fileset consists of ..."
    entry.gcs_fileset_spec.file_patterns.append("gs://my_bucket/*")
    entry.type_ = datacatalog_v1beta1.EntryType.FILESET

    # Create the Schema, for example when you have a csv file.
    columns = []
    columns.append(
        datacatalog_v1beta1.types.ColumnSchema(
            column="first_name",
            description="First name",
            mode="REQUIRED",
            type_="STRING",
        )
    )

    columns.append(
        datacatalog_v1beta1.types.ColumnSchema(
            column="last_name", description="Last name", mode="REQUIRED", type_="STRING"
        )
    )

    # Create sub columns for the addresses parent column
    subcolumns = []
    subcolumns.append(
        datacatalog_v1beta1.types.ColumnSchema(
            column="city", description="City", mode="NULLABLE", type_="STRING"
        )
    )

    subcolumns.append(
        datacatalog_v1beta1.types.ColumnSchema(
            column="state", description="State", mode="NULLABLE", type_="STRING"
        )
    )

    columns.append(
        datacatalog_v1beta1.types.ColumnSchema(
            column="addresses",
            description="Addresses",
            mode="REPEATED",
            subcolumns=subcolumns,
            type_="RECORD",
        )
    )

    entry.schema.columns.extend(columns)

    # Send the entry to the API for creation.
    # Raises google.api_core.exceptions.AlreadyExists if the Entry already
    # exists within the project.
    entry = client.create_entry(
        request={"parent": entry_group_name, "entry_id": entry_id, "entry": entry}
    )
    print("Created entry {}".format(entry.name))
    # [END data_catalog_create_fileset_v1beta1]
