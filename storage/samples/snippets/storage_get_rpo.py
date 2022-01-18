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

"""Sample that gets RPO (Recovery Point Objective) of a bucket
This sample is used on this page:
    https://cloud.google.com/storage/docs/managing-turbo-replication
For more information, see README.md.
"""

# [START storage_get_rpo]

from google.cloud import storage
from google.cloud.storage.constants import RPO_DEFAULT


def get_rpo(bucket_name):
    """Gets the RPO of the bucket"""
    # The ID of your GCS bucket
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.rpo = RPO_DEFAULT
    rpo = bucket.rpo

    print(f"RPO for {bucket.name} is {rpo}.")


# [END storage_get_rpo]

if __name__ == "__main__":
    get_rpo(bucket_name=sys.argv[1])
