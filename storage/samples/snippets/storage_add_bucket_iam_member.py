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

# [START storage_add_bucket_iam_member]
from google.cloud import storage


def add_bucket_iam_member(bucket_name, role, member):
    """Add a new member to an IAM Policy"""
    # bucket_name = "your-bucket-name"
    # role = "IAM role, e.g., roles/storage.objectViewer"
    # member = "IAM identity, e.g., user: name@example.com"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)

    policy.bindings.append({"role": role, "members": {member}})

    bucket.set_iam_policy(policy)

    print("Added {} with role {} to {}.".format(member, role, bucket_name))


# [END storage_add_bucket_iam_member]


if __name__ == "__main__":
    add_bucket_iam_member(bucket_name=sys.argv[1], role=sys.argv[2], member=sys.argv[3])
