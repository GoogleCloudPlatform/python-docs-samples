#!/usr/bin/env python

# Copyright 2019 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

# [START storage_remove_bucket_default_owner]
from google.cloud import storage


def remove_bucket_default_owner(bucket_name, user_email):
    """Removes a user from the access control list of the given bucket's
    default object access control list."""
    # bucket_name = "your-bucket-name"
    # user_email = "name@example.com"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Reload fetches the current ACL from Cloud Storage.
    bucket.acl.reload()

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # remove access for different types of entities.
    bucket.default_object_acl.user(user_email).revoke_read()
    bucket.default_object_acl.user(user_email).revoke_write()
    bucket.default_object_acl.user(user_email).revoke_owner()
    bucket.default_object_acl.save()

    print(
        "Removed user {} from the default acl of bucket {}.".format(
            user_email, bucket_name
        )
    )


# [END storage_remove_bucket_default_owner]

if __name__ == "__main__":
    remove_bucket_default_owner(
        bucket_name=sys.argv[1], user_email=sys.argv[2]
    )
