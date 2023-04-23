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


def create_entry_group(project_id, entry_group_id):
    # [START data_catalog_create_entry_group_v1beta1]
    from google.cloud import datacatalog_v1beta1

    client = datacatalog_v1beta1.DataCatalogClient()

    # TODO(developer): Set entry_group_id to the ID of the
    #  entry group to create.
    # project_id = "your-project-id"

    # TODO(developer): Specify the geographic location where the
    #  entry group should reside.
    # Currently, Data Catalog stores metadata in the us-central1 region.
    location_id = "us-central1"

    # TODO(developer): Set entry_group_id to the ID of the
    #  entry group to create.
    # entry_group_id = "your_entry_group_id"

    # Construct a full location path to be the parent of the entry group.
    parent = f"projects/{project_id}/locations/{location_id}"

    # Construct a full EntryGroup object to send to the API.
    entry_group = datacatalog_v1beta1.EntryGroup()
    entry_group.display_name = "My Entry Group"
    entry_group.description = "This Entry Group consists of ..."

    # Send the entry group to the API for creation.
    # Raises google.api_core.exceptions.AlreadyExists if the Entry Group
    # already exists within the project.
    entry_group = client.create_entry_group(
        request={
            "parent": parent,
            "entry_group_id": entry_group_id,
            "entry_group": entry_group,
        }
    )  # Make an API request.
    print(f"Created entry group {entry_group.name}")
    # [END data_catalog_create_entry_group_v1beta1]
