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

# [START dataplex_delete_data_profile_scan]
import sys

from google.api_core import exceptions
from google.cloud import dataplex_v1


def delete_data_profile_scan(
    project_id: str,
    location: str,
    data_scan_id: str,
) -> None:
    """Deletes a Dataplex data profile scan resource.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        location: Google Cloud region where the data scan resides
            (for example, 'us-central1').
        data_scan_id: Dataplex data profile scan ID to delete
            (for example, 'example-profile-scan').
    """
    client = dataplex_v1.DataScanServiceClient()
    scan_name = f"projects/{project_id}/locations/{location}/dataScans/{data_scan_id}"
    # Deleting a DataScan is a long-running operation that removes the scan configuration.
    request = dataplex_v1.DeleteDataScanRequest(name=scan_name)

    try:
        print(f"Deleting Dataplex data profile scan: {scan_name}")
        operation = client.delete_data_scan(request=request)
        operation.result()
    except exceptions.NotFound as err:
        print(
            f"error: data profile scan '{data_scan_id}' not found in location "
            f"'{location}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to delete data profile scan '{data_scan_id}' in location "
            f"'{location}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {scan_name}")
    print("Deleted: True")
    print(f"Operation Completed: {operation.done()}")


# [END dataplex_delete_data_profile_scan]
