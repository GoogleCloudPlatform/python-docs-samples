#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
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

# [START storage_set_bucket_default_kms_key]
from google.cloud import storage


def enable_default_kms_key(bucket_name, kms_key_name):
    """Sets a bucket's default KMS key."""
    # bucket_name = "your-bucket-name"
    # kms_key_name = "projects/PROJ/locations/LOC/keyRings/RING/cryptoKey/KEY"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.default_kms_key_name = kms_key_name
    bucket.patch()

    print(
        "Set default KMS key for bucket {} to {}.".format(
            bucket.name, bucket.default_kms_key_name
        )
    )


# [END storage_set_bucket_default_kms_key]

if __name__ == "__main__":
    enable_default_kms_key(bucket_name=sys.argv[1], kms_key_name=sys.argv[2])
