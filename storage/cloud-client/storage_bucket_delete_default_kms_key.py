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

# [START storage_bucket_delete_default_kms_key]
from google.cloud import storage


def bucket_delete_default_kms_key(bucket_name):
    """Delete a default KMS key of bucket"""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.default_kms_key_name = None
    bucket.patch()

    print("Default KMS key was removed from {}".format(bucket.name))
    return bucket


# [END storage_bucket_delete_default_kms_key]

if __name__ == "__main__":
    bucket_delete_default_kms_key(bucket_name=sys.argv[1])
