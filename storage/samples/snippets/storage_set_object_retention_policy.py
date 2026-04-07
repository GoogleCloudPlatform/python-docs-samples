#!/usr/bin/env python

# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import sys

# [START storage_set_object_retention_policy]
from google.cloud import storage


def set_object_retention_policy(bucket_name, contents, destination_blob_name):
    """Set the object retention policy of a file."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents)

    # Set the retention policy for the file.
    blob.retention.mode = "Unlocked"
    retention_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10)
    blob.retention.retain_until_time = retention_date
    blob.patch()
    print(
        f"Retention policy for file {destination_blob_name} was set to: {blob.retention.mode}."
    )

    # To modify an existing policy on an unlocked file object, pass in the override parameter.
    new_retention_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=9)
    blob.retention.retain_until_time = new_retention_date
    blob.patch(override_unlocked_retention=True)
    print(
        f"Retention policy for file {destination_blob_name} was updated to: {blob.retention.retain_until_time}."
    )


# [END storage_set_object_retention_policy]


if __name__ == "__main__":
    set_object_retention_policy(
        bucket_name=sys.argv[1],
        contents=sys.argv[2],
        destination_blob_name=sys.argv[3],
    )
