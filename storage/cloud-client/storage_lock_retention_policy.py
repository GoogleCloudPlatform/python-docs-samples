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

# [START storage_lock_retention_policy]
from google.cloud import storage


def lock_retention_policy(bucket_name):
    """Locks the retention policy on a given bucket"""
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    # get_bucket gets the current metageneration value for the bucket,
    # required by lock_retention_policy.
    bucket = storage_client.get_bucket(bucket_name)

    # Warning: Once a retention policy is locked it cannot be unlocked
    # and retention period can only be increased.
    bucket.lock_retention_policy()

    print("Retention policy for {} is now locked".format(bucket_name))
    print(
        "Retention policy effective as of {}".format(
            bucket.retention_policy_effective_time
        )
    )


# [END storage_lock_retention_policy]


if __name__ == "__main__":
    lock_retention_policy(bucket_name=sys.argv[1])
