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

# [START storage_get_retention_policy]
from google.cloud import storage


def get_retention_policy(bucket_name):
    """Gets the retention policy on a given bucket"""
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.reload()

    print("Retention Policy for {}".format(bucket_name))
    print("Retention Period: {}".format(bucket.retention_period))
    if bucket.retention_policy_locked:
        print("Retention Policy is locked")

    if bucket.retention_policy_effective_time:
        print(
            "Effective Time: {}".format(bucket.retention_policy_effective_time)
        )


# [END storage_get_retention_policy]


if __name__ == "__main__":
    get_retention_policy(bucket_name=sys.argv[1])
