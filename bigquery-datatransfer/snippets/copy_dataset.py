# Copyright 2020 Google LLC
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


def copy_dataset(override_values={}):
    # [START bigquerydatatransfer_copy_dataset]
    from google.cloud import bigquery_datatransfer

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    destination_project_id = "my-destination-project"
    destination_dataset_id = "my_destination_dataset"
    source_project_id = "my-source-project"
    source_dataset_id = "my_source_dataset"
    # [END bigquerydatatransfer_copy_dataset]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    destination_project_id = override_values.get(
        "destination_project_id", destination_project_id
    )
    destination_dataset_id = override_values.get(
        "destination_dataset_id", destination_dataset_id
    )
    source_project_id = override_values.get("source_project_id", source_project_id)
    source_dataset_id = override_values.get("source_dataset_id", source_dataset_id)
    # [START bigquerydatatransfer_copy_dataset]
    transfer_config = bigquery_datatransfer.TransferConfig(
        destination_dataset_id=destination_dataset_id,
        display_name="Your Dataset Copy Name",
        data_source_id="cross_region_copy",
        params={
            "source_project_id": source_project_id,
            "source_dataset_id": source_dataset_id,
        },
        schedule="every 24 hours",
    )
    transfer_config = transfer_client.create_transfer_config(
        parent=transfer_client.common_project_path(destination_project_id),
        transfer_config=transfer_config,
    )
    print(f"Created transfer config: {transfer_config.name}")
    # [END bigquerydatatransfer_copy_dataset]
    return transfer_config
