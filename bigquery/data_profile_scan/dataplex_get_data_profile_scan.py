# Copyright 2026 Google LLC
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

# [START dataplex_get_data_profile_scan]
import sys

from google.api_core import exceptions
from google.cloud import dataplex_v1


def get_data_profile_scan(
    project_id: str,
    location: str,
    data_scan_id: str,
) -> None:
    """Retrieves a Dataplex data profile scan and its latest profile results.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        location: Google Cloud region where the data scan resides
            (for example, 'us-central1').
        data_scan_id: Dataplex data profile scan ID
            (for example, 'example-profile-scan').
    """
    client = dataplex_v1.DataScanServiceClient()
    scan_name = f"projects/{project_id}/locations/{location}/dataScans/{data_scan_id}"
    # Request DataScanView.FULL so the response includes data_profile_result metrics.
    request = dataplex_v1.GetDataScanRequest(
        name=scan_name,
        view=dataplex_v1.GetDataScanRequest.DataScanView.FULL,
    )

    try:
        scan = client.get_data_scan(request=request)
    except exceptions.NotFound as err:
        print(
            f"error: data profile scan '{data_scan_id}' not found in location "
            f"'{location}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to retrieve data profile scan '{data_scan_id}' in location "
            f"'{location}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    row_count = (
        scan.data_profile_result.row_count if scan.data_profile_result else "N/A"
    )
    print(f"Resource ID: {scan.name}")
    print(f"Data Resource: {scan.data.resource}")
    print(f"Row Count: {row_count}")
    print(f"Scan State: {scan.state.name}")


# [END dataplex_get_data_profile_scan]
