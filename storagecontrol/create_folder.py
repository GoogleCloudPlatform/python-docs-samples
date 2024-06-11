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

# [START storage_control_create_folder]
from google.cloud import storage_control_v2


def create_folder(bucket_name: str, folder_name: str) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    # The name of the folder to be created
    # folder_name = "folder-name"

    storage_control_client = storage_control_v2.StorageControlClient()
    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    project_path = storage_control_client.common_project_path("_")
    bucket_path = f"{project_path}/buckets/{bucket_name}"

    request = storage_control_v2.CreateFolderRequest(
        parent=bucket_path,
        folder_id=folder_name,
    )
    response = storage_control_client.create_folder(request=request)

    print(f"Created folder: {response.name}")


# [END storage_control_create_folder]


if __name__ == "__main__":
    create_folder(bucket_name=sys.argv[1], folder_name=sys.argv[2])
