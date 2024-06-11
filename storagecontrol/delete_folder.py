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

# [START storage_control_delete_folder]
from google.cloud import storage_control_v2


def delete_folder(bucket_name: str, folder_name: str) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    # The name of the folder to be deleted
    # folder_name = "folder-name"

    storage_control_client = storage_control_v2.StorageControlClient()
    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    folder_path = storage_control_client.folder_path(
        project="_", bucket=bucket_name, folder=folder_name
    )

    request = storage_control_v2.DeleteFolderRequest(
        name=folder_path,
    )
    storage_control_client.delete_folder(request=request)

    print(f"Deleted folder {folder_name}")


# [END storage_control_delete_folder]


if __name__ == "__main__":
    delete_folder(bucket_name=sys.argv[1], folder_name=sys.argv[2])
