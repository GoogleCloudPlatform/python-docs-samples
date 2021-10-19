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

# [START storage_view_bucket_iam_members]
from google.cloud import storage


def view_bucket_iam_members(bucket_name):
    """View IAM Policy for a bucket"""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)

    for binding in policy.bindings:
        print("Role: {}, Members: {}".format(binding["role"], binding["members"]))


# [END storage_view_bucket_iam_members]


if __name__ == "__main__":
    view_bucket_iam_members(bucket_name=sys.argv[1])
