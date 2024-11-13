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

# [START storage_control_managed_folder_delete]
from google.cloud import storage_control_v2


def delete_managed_folder(bucket_name: str, managed_folder_id: str) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    # The name of the managed folder to be deleted
    # managed_folder_id = "managed-folder-name"

    storage_control_client = storage_control_v2.StorageControlClient()
    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    folder_path = storage_control_client.managed_folder_path(
        "_", bucket_name, managed_folder_id
    )

    request = storage_control_v2.DeleteManagedFolderRequest(
        name=folder_path,
    )
    storage_control_client.delete_managed_folder(request=request)

    print(f"Deleted managed folder: {managed_folder_id}")


# [END storage_control_managed_folder_delete]


if __name__ == "__main__":
    delete_managed_folder(bucket_name=sys.argv[1], managed_folder_id=sys.argv[2])
