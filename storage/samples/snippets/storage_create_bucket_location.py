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

"""Sample that creates a new bucket in a specified region
"""

# [START storage_create_bucket_location]

from google.cloud import storage


def create_bucket_location(bucket_name, bucket_location):
    """Creates bucket in specified region."""
    # The ID of your GCS bucket
    # bucket_name = "my-bucket"
    # bucket_location = 'us-west1' # region
    # bucket_location = 'nam4' # dual-region
    # bucket_location = 'us' #multi-region

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.create(location=bucket_location)

    print(f"{bucket.name} created in {bucket.location}.")


# [END storage_create_bucket_location]

if __name__ == "__main__":
    create_bucket_location(bucket_name=sys.argv[1], bucket_location=sys.argv[2])
