#!/usr/bin/env python

# Copyright 2020 Google LLC. All Rights Reserved
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

# [START storage_add_bucket_conditional_iam_binding]
from google.cloud import storage


def add_bucket_conditional_iam_binding(
    bucket_name, role, title, description, expression, members
):
    """Add a conditional IAM binding to a bucket's IAM policy."""
    # bucket_name = "your-bucket-name"
    # role = "IAM role, e.g. roles/storage.objectViewer"
    # members = {"IAM identity, e.g. user: name@example.com}"
    # title = "Condition title."
    # description = "Condition description."
    # expression = "Condition expression."

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)

    # Set the policy's version to 3 to use condition in bindings.
    policy.version = 3

    policy.bindings.append(
        {
            "role": role,
            "members": members,
            "condition": {
                "title": title,
                "description": description,
                "expression": expression,
            },
        }
    )

    bucket.set_iam_policy(policy)

    print("Added the following member(s) with role {} to {}:".format(role, bucket_name))

    for member in members:
        print("    {}".format(member))

    print("with condition:")
    print("    Title: {}".format(title))
    print("    Description: {}".format(description))
    print("    Expression: {}".format(expression))


# [END storage_add_bucket_conditional_iam_binding]


if __name__ == "__main__":
    add_bucket_conditional_iam_binding(
        bucket_name=sys.argv[1],
        role=sys.argv[2],
        title=sys.argv[3],
        description=sys.argv[4],
        expression=sys.argv[5],
        members=set(sys.argv[6::]),
    )
