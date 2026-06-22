# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START dataplex_create_data_quality_scan_global]
import google.api_core.exceptions
from google.cloud import dataplex_v1


def create_data_quality_scan_global(
    project_id: str,
    dataset_id: str,
    table_id: str,
    location: str,
    column_id_1: str,
    column_id_2: str,
) -> None:
    """Creates a Dataplex Data Quality Scan using global API endpoint routing.

    Args:
        project_id (str): Google Cloud Platform project ID where the scan is created.
        dataset_id (str): Target BigQuery dataset ID.
        table_id (str): Target BigQuery table ID to scan.
        location (str): Google Cloud Platform region where serverless compute runs.
        column_id_1 (str): Name of the first column to evaluate.
        column_id_2 (str): Name of the second column to evaluate.
    """
    client = dataplex_v1.DataScanServiceClient()

    parent = client.common_location_path(project=project_id, location=location)

    # A bigquery table with at least 2 columns is assumed.
    bigquery_table = (
        f"//bigquery.googleapis.com/projects/{project_id}"
        f"/datasets/{dataset_id}/tables/{table_id}"
    )

    data_quality_spec = dataplex_v1.DataQualitySpec(
        rules=[
            dataplex_v1.DataQualityRule(
                name="global-null-assertion",
                dimension="COMPLETENESS",
                description="Fails if any row contains a null value",
                sql_assertion=dataplex_v1.DataQualityRule.SqlAssertion(
                    # Use ${data()} as the placeholder for the table Dataplex is scanning
                    sql_statement=(
                        "SELECT * FROM ${data()} "
                        f"WHERE {column_id_1} IS NULL OR {column_id_2} IS NULL"
                    )
                ),
            )
        ]
    )

    data_scan = dataplex_v1.DataScan(
        display_name="Global Data Quality Scan",
        data=dataplex_v1.DataSource(resource=bigquery_table),
        data_quality_spec=data_quality_spec,
    )

    request = dataplex_v1.CreateDataScanRequest(parent=parent, data_scan=data_scan)

    try:
        operation = client.create_data_scan(request=request)
        print(operation.result())
    except google.api_core.exceptions.AlreadyExists:
        print("A scan with this ID already exists.")
    except google.api_core.exceptions.InvalidArgument as e:
        print(f"Your scan configuration is invalid: {e}")
    except google.api_core.exceptions.GoogleAPIError as e:
        print(f"Unexpected exception: {e}")

# [END dataplex_create_data_quality_scan_global]
