#!/usr/bin/env python

# Copyright 2021 Google LLC
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

"""Sample that sets the replication behavior or recovery point objective (RPO) to default.
This sample is used on this page:
    https://cloud.google.com/storage/docs/managing-turbo-replication
For more information, see README.md.
"""

# [START storage_set_rpo_default]

from google.cloud import storage
from google.cloud.storage.constants import RPO_DEFAULT


def set_rpo_default(bucket_name):
    """Sets the RPO to DEFAULT, disabling the turbo replication feature"""
    # The ID of your GCS bucket
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.rpo = RPO_DEFAULT
    bucket.patch()

    print(f"RPO is set to DEFAULT for {bucket.name}.")


# [END storage_set_rpo_default]

if __name__ == "__main__":
    set_rpo_default(bucket_name=sys.argv[1])
