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

# [START storage_set_retention_policy]
from google.cloud import storage


def set_retention_policy(bucket_name, retention_period):
    """Defines a retention policy on a given bucket"""
    # bucket_name = "my-bucket"
    # retention_period = 10

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.retention_period = retention_period
    bucket.patch()

    print(
        "Bucket {} retention period set for {} seconds".format(
            bucket.name, bucket.retention_period
        )
    )


# [END storage_set_retention_policy]


if __name__ == "__main__":
    set_retention_policy(bucket_name=sys.argv[1], retention_period=sys.argv[2])
