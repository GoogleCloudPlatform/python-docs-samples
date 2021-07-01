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

# [START storage_set_public_access_prevention_enforced]
from google.cloud import storage
from google.cloud.storage.constants import PUBLIC_ACCESS_PREVENTION_ENFORCED


def set_public_access_prevention_enforced(bucket_name):
    """Enforce public access prevention for a bucket."""
    # The ID of your GCS bucket
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    bucket.iam_configuration.public_access_prevention = (
        PUBLIC_ACCESS_PREVENTION_ENFORCED
    )
    bucket.patch()

    print(f"Public access prevention is set to enforced for {bucket.name}.")


# [END storage_set_public_access_prevention_enforced]

if __name__ == "__main__":
    set_public_access_prevention_enforced(bucket_name=sys.argv[1])
