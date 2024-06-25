# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

# [START storage_control_managed_folder_list]
from google.cloud import storage_control_v2


def list_managed_folders(bucket_name: str) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    storage_control_client = storage_control_v2.StorageControlClient()
    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    project_path = storage_control_client.common_project_path("_")
    bucket_path = f"{project_path}/buckets/{bucket_name}"

    request = storage_control_v2.ListManagedFoldersRequest(
        parent=bucket_path,
    )

    page_result = storage_control_client.list_managed_folders(request=request)
    for managed_folder in page_result:
        print(managed_folder)

    print(f"Listed managed folders in bucket {bucket_name}")


# [END storage_control_managed_folder_list]


if __name__ == "__main__":
    list_managed_folders(bucket_name=sys.argv[1])
