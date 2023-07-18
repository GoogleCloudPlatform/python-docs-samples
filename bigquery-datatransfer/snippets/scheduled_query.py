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


def create_scheduled_query(override_values={}):
    # [START bigquerydatatransfer_create_scheduled_query]
    # [START bigquerydatatransfer_create_scheduled_query_with_service_account]
    from google.cloud import bigquery_datatransfer

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    # The project where the query job runs is the same as the project
    # containing the destination dataset.
    project_id = "your-project-id"
    dataset_id = "your_dataset_id"

    # This service account will be used to execute the scheduled queries. Omit
    # this request parameter to run the query as the user with the credentials
    # associated with this client.
    service_account_name = "abcdef-test-sa@abcdef-test.iam.gserviceaccount.com"
    # [END bigquerydatatransfer_create_scheduled_query_with_service_account]
    # [END bigquerydatatransfer_create_scheduled_query]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = override_values.get("project_id", project_id)
    dataset_id = override_values.get("dataset_id", dataset_id)
    service_account_name = override_values.get(
        "service_account_name", service_account_name
    )
    # [START bigquerydatatransfer_create_scheduled_query]
    # [START bigquerydatatransfer_create_scheduled_query_with_service_account]

    # Use standard SQL syntax for the query.
    query_string = """
    SELECT
      CURRENT_TIMESTAMP() as current_time,
      @run_time as intended_run_time,
      @run_date as intended_run_date,
      17 as some_integer
    """

    parent = transfer_client.common_project_path(project_id)

    transfer_config = bigquery_datatransfer.TransferConfig(
        destination_dataset_id=dataset_id,
        display_name="Your Scheduled Query Name",
        data_source_id="scheduled_query",
        params={
            "query": query_string,
            "destination_table_name_template": "your_table_{run_date}",
            "write_disposition": "WRITE_TRUNCATE",
            "partitioning_field": "",
        },
        schedule="every 24 hours",
    )

    transfer_config = transfer_client.create_transfer_config(
        bigquery_datatransfer.CreateTransferConfigRequest(
            parent=parent,
            transfer_config=transfer_config,
            service_account_name=service_account_name,
        )
    )

    print("Created scheduled query '{}'".format(transfer_config.name))
    # [END bigquerydatatransfer_create_scheduled_query_with_service_account]
    # [END bigquerydatatransfer_create_scheduled_query]
    # Return the config name for testing purposes, so that it can be deleted.
    return transfer_config
