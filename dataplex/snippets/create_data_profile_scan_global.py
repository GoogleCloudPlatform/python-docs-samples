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

# [START dataplex_create_data_profile_scan_global]
import google.api_core.exceptions
from google.cloud import dataplex_v1


def create_data_profile_scan_global(
    project_id: str,
    dataset_id: str,
    table_id: str,
    location: str,
) -> None:
    """Creates a Dataplex Data Profile Scan using global API endpoint routing.

    Args:
        project_id (str): Google Cloud Platform project ID where the scan is created.
        dataset_id (str): Target BigQuery dataset ID.
        table_id (str): Target BigQuery table ID to scan.
        location (str): Google Cloud Platform region where serverless compute runs.
    """
    client = dataplex_v1.DataScanServiceClient()

    parent = client.common_location_path(project=project_id, location=location)

    bigquery_table = (
        f"//bigquery.googleapis.com/projects/{project_id}"
        f"/datasets/{dataset_id}/tables/{table_id}"
    )

    data_profile_spec = dataplex_v1.DataProfileSpec(sampling_percent=100.0)

    data_scan = dataplex_v1.DataScan(
        display_name="Global Data Profile Scan",
        description="Regional data profile scan generating automated table statistics.",
        data=dataplex_v1.DataSource(resource=bigquery_table),
        data_profile_spec=data_profile_spec,
    )

    request = dataplex_v1.CreateDataScanRequest(
        parent=parent,
        data_scan=data_scan,
    )

    try:
        operation = client.create_data_scan(request=request)
        print(operation.result())

    except google.api_core.exceptions.AlreadyExists:
        print("A scan with this ID already exists.")
    except google.api_core.exceptions.InvalidArgument as e:
        print(f"Your scan configuration is invalid: {e}")
    except google.api_core.exceptions.GoogleAPIError as e:
        print(f"Unexpected exception: {e}")


# [END dataplex_create_data_profile_scan_global]
