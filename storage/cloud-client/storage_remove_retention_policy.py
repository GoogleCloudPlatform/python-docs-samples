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

# [START storage_remove_retention_policy]
from google.cloud import storage


def remove_retention_policy(bucket_name):
    """Removes the retention policy on a given bucket"""
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.reload()

    if bucket.retention_policy_locked:
        print(
            "Unable to remove retention period as retention policy is locked."
        )
        return

    bucket.retention_period = None
    bucket.patch()

    print("Removed bucket {} retention policy".format(bucket.name))


# [END storage_remove_retention_policy]


if __name__ == "__main__":
    remove_retention_policy(bucket_name=sys.argv[1])
