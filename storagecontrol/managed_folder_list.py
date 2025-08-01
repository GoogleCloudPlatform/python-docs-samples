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

# [START storage_control_managed_folder_list]
from google.cloud import storage_control_v2


def list_managed_folders(bucket_name: str = "your-bucket-name") -> None:
    """Lists all managed folders in a Google Cloud Storage bucket.

    Args:
        bucket_name: The name of the Google Cloud Storage bucket.

    Returns:
        None. The function prints the name of each managed folder to the
        console.

    Example:
        >>> list_managed_folders(bucket_name="my-test-bucket")
        Managed folders in bucket projects/_/buckets/my-test-bucket:
            projects/_/buckets/my-test-bucket/managedFolders/folder-one
            projects/_/buckets/my-test-bucket/managedFolders/folder-two
    """
    client = storage_control_v2.StorageControlClient()

    # The storage bucket path uses the global access pattern,
    # in which the "_" denotes this bucket exists in the global namespace.
    GLOBAL_NAMESPACE_PATTERN = "_"
    bucket_resource_name = f"projects/{GLOBAL_NAMESPACE_PATTERN}/buckets/{bucket_name}"

    managed_folders = client.list_managed_folders(parent=bucket_resource_name)

    print(f"Managed folders in bucket {bucket_resource_name}:")
    for managed_folder in managed_folders:
        print(f"\t{managed_folder.name}")
# [END storage_control_managed_folder_list]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "bucket_name",
        help="The name of the GCS bucket.",
    )

    args = parser.parse_args()

    list_managed_folders(args.bucket_name)
