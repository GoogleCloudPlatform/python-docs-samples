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

# [START storage_list_hmac_keys]
from google.cloud import storage


def list_keys(project_id):
    """
    List all HMAC keys associated with the project.
    """
    # project_id = "Your Google Cloud project ID"

    storage_client = storage.Client(project=project_id)
    hmac_keys = storage_client.list_hmac_keys(project_id=project_id)
    print("HMAC Keys:")
    for hmac_key in hmac_keys:
        print(
            "Service Account Email: {}".format(hmac_key.service_account_email)
        )
        print("Access ID: {}".format(hmac_key.access_id))
    return hmac_keys


# [END storage_list_hmac_keys]

if __name__ == "__main__":
    list_keys(project_id=sys.argv[1])
