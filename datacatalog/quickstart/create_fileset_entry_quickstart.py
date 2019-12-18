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


def create_fileset_entry_quickstart(client, project_id, entry_group_id, entry_id):

    # [START datacatalog_create_fileset_quickstart_tag]
    # Import required modules.
    from google.cloud import datacatalog_v1beta1

    # TODO(developer): Construct a Data Catalog client object.
    # client = datacatalog_v1beta1.DataCatalogClient()

    # TODO(developer): Set project_id to your
    #  Google Cloud Platform project ID the entry will belong.
    # project_id = "your-project-id"

    # TODO(developer): Specify the geographic location where the
    #  entry should reside.
    # Currently, Data Catalog stores metadata in the us-central1 region.
    location_id = "us-central1"

    # TODO(developer): Set entry_group_id to the ID of the entry group
    #  the entry will belong.
    # entry_group_id = "your_entry_group_id"

    # TODO(developer): Set entry_id to the ID of the entry to create.
    # entry_id = "your_entry_id"

    # Create an Entry Group.
    # Construct a full Entry Group object to send to the API.
    entry_group_obj = datacatalog_v1beta1.types.EntryGroup()
    entry_group_obj.display_name = "My Fileset Entry Group"
    entry_group_obj.description = "This Entry Group consists of ...."

    # Send the Entry Group to the API for creation.
    # Raises google.api_core.exceptions.AlreadyExists if the Entry Group
    # already exists within the project.
    entry_group = client.create_entry_group(
        parent=datacatalog_v1beta1.DataCatalogClient.location_path(
            project_id, location_id
        ),
        entry_group_id=entry_group_id,
        entry_group=entry_group_obj,
    )
    print("Created entry group {}".format(entry_group.name))

    # Create a Fileset Entry.
    # Construct a full Entry object to send to the API.
    entry = datacatalog_v1beta1.types.Entry()
    entry.display_name = "My Fileset"
    entry.description = "This Fileset consists of ..."
    entry.gcs_fileset_spec.file_patterns.append("gs://cloud-samples-data/*")
    entry.type = datacatalog_v1beta1.enums.EntryType.FILESET

    # Create the Schema, for example when you have a csv file.
    columns = []
    columns.append(
        datacatalog_v1beta1.types.ColumnSchema(
            column="first_name",
            description="First name",
            mode="REQUIRED",
            type="STRING",
        )
    )

    columns.append(
        datacatalog_v1beta1.types.ColumnSchema(
            column="last_name", description="Last name", mode="REQUIRED", type="STRING"
        )
    )

    # Create sub columns for the addresses parent column
    subcolumns = []
    subcolumns.append(
        datacatalog_v1beta1.types.ColumnSchema(
            column="city", description="City", mode="NULLABLE", type="STRING"
        )
    )

    subcolumns.append(
        datacatalog_v1beta1.types.ColumnSchema(
            column="state", description="State", mode="NULLABLE", type="STRING"
        )
    )

    columns.append(
        datacatalog_v1beta1.types.ColumnSchema(
            column="addresses",
            description="Addresses",
            mode="REPEATED",
            subcolumns=subcolumns,
            type="RECORD",
        )
    )

    entry.schema.columns.extend(columns)

    # Send the entry to the API for creation.
    # Raises google.api_core.exceptions.AlreadyExists if the Entry already
    # exists within the project.
    entry = client.create_entry(entry_group.name, entry_id, entry)
    print("Created entry {}".format(entry.name))
    # [END datacatalog_create_fileset_quickstart_tag]
