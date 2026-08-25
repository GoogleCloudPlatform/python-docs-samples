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

# [START storage_control_rename_folder]
from google.cloud import storage_control_v2


def rename_folder(
    bucket_name: str, source_folder_name: str, destination_folder_name: str
) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"
    #
    # The source folder ID
    # source_folder_name = "current-folder-name"
    #
    # The destination folder ID
    # destination_folder_name = "new-folder-name"

    storage_control_client = storage_control_v2.StorageControlClient()
    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    source_folder_path = storage_control_client.folder_path(
        project="_", bucket=bucket_name, folder=source_folder_name
    )

    request = storage_control_v2.RenameFolderRequest(
        name=source_folder_path,
        destination_folder_id=destination_folder_name,
    )

    operation = storage_control_client.rename_folder(request=request)
    operation.result(60)

    print(f"Renamed folder {source_folder_name} to {destination_folder_name}")


# [END storage_control_rename_folder]


if __name__ == "__main__":
    rename_folder(
        bucket_name=sys.argv[1],
        source_folder_name=sys.argv[2],
        destination_folder_name=sys.argv[3],
    )
