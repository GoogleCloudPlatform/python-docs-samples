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

"""Sample that creates a new bucket with dual-region and turbo replication.
This sample is used on this page:
    https://cloud.google.com/storage/docs/managing-turbo-replication
For more information, see README.md.
"""

# [START storage_create_bucket_turbo_replication]

from google.cloud import storage
from google.cloud.storage.constants import RPO_ASYNC_TURBO


def create_bucket_turbo_replication(bucket_name):
    """Creates dual-region bucket with turbo replication enabled."""
    # The ID of your GCS bucket
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.location = "NAM4"
    bucket.rpo = RPO_ASYNC_TURBO
    bucket.create()

    print(f"{bucket.name} created with the recovery point objective (RPO) set to {bucket.rpo} in {bucket.location}.")


# [END storage_create_bucket_turbo_replication]

if __name__ == "__main__":
    create_bucket_turbo_replication(bucket_name=sys.argv[1])
