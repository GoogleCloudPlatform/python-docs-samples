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


def list_configs(override_values={}):
    # [START bigquerydatatransfer_list_configs]
    from google.cloud import bigquery_datatransfer

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    project_id = "my-project"
    # [END bigquerydatatransfer_list_configs]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = override_values.get("project_id", project_id)
    # [START bigquerydatatransfer_list_configs]
    parent = transfer_client.common_project_path(project_id)

    configs = transfer_client.list_transfer_configs(parent=parent)
    print("Got the following configs:")
    for config in configs:
        print(f"\tID: {config.name}, Schedule: {config.schedule}")
    # [END bigquerydatatransfer_list_configs]


def update_config(override_values={}):
    # [START bigquerydatatransfer_update_config]
    from google.cloud import bigquery_datatransfer
    from google.protobuf import field_mask_pb2

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    transfer_config_name = "projects/1234/locations/us/transferConfigs/abcd"
    new_display_name = "My Transfer Config"
    # [END bigquerydatatransfer_update_config]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    new_display_name = override_values.get("new_display_name", new_display_name)
    transfer_config_name = override_values.get(
        "transfer_config_name", transfer_config_name
    )
    # [START bigquerydatatransfer_update_config]

    transfer_config = bigquery_datatransfer.TransferConfig(name=transfer_config_name)
    transfer_config.display_name = new_display_name

    transfer_config = transfer_client.update_transfer_config(
        {
            "transfer_config": transfer_config,
            "update_mask": field_mask_pb2.FieldMask(paths=["display_name"]),
        }
    )

    print(f"Updated config: '{transfer_config.name}'")
    print(f"New display name: '{transfer_config.display_name}'")
    # [END bigquerydatatransfer_update_config]
    # Return the config name for testing purposes, so that it can be deleted.
    return transfer_config


def update_credentials_with_service_account(override_values={}):
    # [START bigquerydatatransfer_update_credentials]
    from google.cloud import bigquery_datatransfer
    from google.protobuf import field_mask_pb2

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    service_account_name = "abcdef-test-sa@abcdef-test.iam.gserviceaccount.com"
    transfer_config_name = "projects/1234/locations/us/transferConfigs/abcd"
    # [END bigquerydatatransfer_update_credentials]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    service_account_name = override_values.get(
        "service_account_name", service_account_name
    )
    transfer_config_name = override_values.get(
        "transfer_config_name", transfer_config_name
    )
    # [START bigquerydatatransfer_update_credentials]

    transfer_config = bigquery_datatransfer.TransferConfig(name=transfer_config_name)

    transfer_config = transfer_client.update_transfer_config(
        {
            "transfer_config": transfer_config,
            "update_mask": field_mask_pb2.FieldMask(paths=["service_account_name"]),
            "service_account_name": service_account_name,
        }
    )

    print("Updated config: '{}'".format(transfer_config.name))
    # [END bigquerydatatransfer_update_credentials]
    # Return the config name for testing purposes, so that it can be deleted.
    return transfer_config


def schedule_backfill(override_values={}):
    # [START bigquerydatatransfer_schedule_backfill]
    import datetime

    from google.cloud import bigquery_datatransfer

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    transfer_config_name = "projects/1234/locations/us/transferConfigs/abcd"
    # [END bigquerydatatransfer_schedule_backfill]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    transfer_config_name = override_values.get(
        "transfer_config_name", transfer_config_name
    )
    # [START bigquerydatatransfer_schedule_backfill]
    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(days=5)
    end_time = now - datetime.timedelta(days=2)

    # Some data sources, such as scheduled_query only support daily run.
    # Truncate start_time and end_time to midnight time (00:00AM UTC).
    start_time = datetime.datetime(
        start_time.year, start_time.month, start_time.day, tzinfo=datetime.timezone.utc
    )
    end_time = datetime.datetime(
        end_time.year, end_time.month, end_time.day, tzinfo=datetime.timezone.utc
    )

    response = transfer_client.schedule_transfer_runs(
        parent=transfer_config_name,
        start_time=start_time,
        end_time=end_time,
    )

    print("Started transfer runs:")
    for run in response.runs:
        print(f"backfill: {run.run_time} run: {run.name}")
    # [END bigquerydatatransfer_schedule_backfill]
    return response.runs


def delete_config(override_values={}):
    # [START bigquerydatatransfer_delete_transfer]
    import google.api_core.exceptions
    from google.cloud import bigquery_datatransfer

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    transfer_config_name = "projects/1234/locations/us/transferConfigs/abcd"
    # [END bigquerydatatransfer_delete_transfer]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    transfer_config_name = override_values.get(
        "transfer_config_name", transfer_config_name
    )
    # [START bigquerydatatransfer_delete_transfer]
    try:
        transfer_client.delete_transfer_config(name=transfer_config_name)
    except google.api_core.exceptions.NotFound:
        print("Transfer config not found.")
    else:
        print(f"Deleted transfer config: {transfer_config_name}")
    # [END bigquerydatatransfer_delete_transfer]
