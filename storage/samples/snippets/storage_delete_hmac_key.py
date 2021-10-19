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

# [START storage_delete_hmac_key]
from google.cloud import storage


def delete_key(access_id, project_id):
    """
    Delete the HMAC key with the given access ID. Key must have state INACTIVE
    in order to succeed.
    """
    # project_id = "Your Google Cloud project ID"
    # access_id = "ID of an HMAC key (must be in INACTIVE state)"

    storage_client = storage.Client(project=project_id)

    hmac_key = storage_client.get_hmac_key_metadata(
        access_id, project_id=project_id
    )
    hmac_key.delete()

    print(
        "The key is deleted, though it may still appear in list_hmac_keys()"
        " results."
    )


# [END storage_delete_hmac_key]

if __name__ == "__main__":
    delete_key(access_id=sys.argv[1], project_id=sys.argv[2])
