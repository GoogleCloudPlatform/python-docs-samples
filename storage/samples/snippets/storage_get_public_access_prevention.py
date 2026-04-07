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

# [START storage_get_public_access_prevention]
from google.cloud import storage


def get_public_access_prevention(bucket_name):
    """Gets the public access prevention setting (either 'inherited' or 'enforced') for a bucket."""
    # The ID of your GCS bucket
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    iam_configuration = bucket.iam_configuration

    print(
        f"Public access prevention is {iam_configuration.public_access_prevention} for {bucket.name}."
    )


# [END storage_get_public_access_prevention]

if __name__ == "__main__":
    get_public_access_prevention(bucket_name=sys.argv[1])
