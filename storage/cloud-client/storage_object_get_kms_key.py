#!/usr/bin/env python

# Copyright 2020 Google LLC. All Rights Reserved.
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

import sys

# [START storage_object_get_kms_key]
from google.cloud import storage


def object_get_kms_key(bucket_name, blob_name):
    """Retrieve the KMS key of a blob"""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)

    kms_key = blob.kms_key_name

    print("The KMS key of a blob is {}".format(blob.kms_key_name))
    return kms_key


# [END storage_object_get_kms_key]

if __name__ == "__main__":
    object_get_kms_key(bucket_name=sys.argv[1], blob_name=sys.argv[2])
