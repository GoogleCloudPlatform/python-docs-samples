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

"""Sample that sets RPO (Recovery Point Objective) to ASYNC_TURBO
This sample is used on this page:
    https://cloud.google.com/storage/docs/managing-turbo-replication
For more information, see README.md.
"""

# [START storage_set_rpo_async_turbo]

from google.cloud import storage
from google.cloud.storage.constants import RPO_ASYNC_TURBO


def set_rpo_async_turbo(bucket_name):
    """Sets the RPO to ASYNC_TURBO, enabling the turbo replication feature"""
    # The ID of your GCS bucket
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.rpo = RPO_ASYNC_TURBO
    bucket.patch()

    print(f"RPO is set to ASYNC_TURBO for {bucket.name}.")


# [END storage_set_rpo_async_turbo]

if __name__ == "__main__":
    set_rpo_async_turbo(bucket_name=sys.argv[1])
