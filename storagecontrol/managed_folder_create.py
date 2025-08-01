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

import argparse

# [START storage_control_managed_folder_create]
from google.cloud import storage_control_v2


def create_managed_folder(
    bucket_name: str = "your-bucket-name",
    managed_folder_name: str = "your-folder-name"
) -> None:
    """Creates a managed folder in a Google Cloud Storage bucket.
    Find more information here:
    https://cloud.google.com/storage/docs/creating-buckets

    A managed folder is a special type of folder
    that can have its own IAM policies and access controls,
    independent of the bucket's policies.

    Args:
        bucket_name: The name of the Google Cloud Storage bucket where the
            managed folder will be created.
        managed_folder_name: The name of the managed folder to be created.

    Returns:
        None. The function prints a success message to the console upon
        successful creation of the managed folder.
    """

    client = storage_control_v2.StorageControlClient()

    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    project_path = client.common_project_path("_")
    bucket_path = f"{project_path}/buckets/{bucket_name}"

    folder = client.create_managed_folder(
            parent=bucket_path,
            managed_folder=storage_control_v2.ManagedFolder(),
            managed_folder_id=managed_folder_name,
        )
    print(f"Created managed folder: {folder.name}")
# [END storage_control_managed_folder_create]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "bucket_name",
        help="The name of the GCS bucket.",
    )
    parser.add_argument(
        "folder_name",
        help="The name of the managed folder to create."
    )

    args = parser.parse_args()

    create_managed_folder(args.bucket_name, args.folder_name)
