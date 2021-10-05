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

"""Sample that sets public access prevention to inherited.
This sample is used on this page:
    https://cloud.google.com/storage/docs/using-public-access-prevention
For more information, see README.md.
"""

# [START storage_set_public_access_prevention_inherited]

from google.cloud import storage
from google.cloud.storage.constants import PUBLIC_ACCESS_PREVENTION_INHERITED


def set_public_access_prevention_inherited(bucket_name):
    """Sets the public access prevention status to inherited, so that the bucket inherits its setting from its parent project."""
    # The ID of your GCS bucket
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    bucket.iam_configuration.public_access_prevention = (
        PUBLIC_ACCESS_PREVENTION_INHERITED
    )
    bucket.patch()

    print(f"Public access prevention is 'inherited' for {bucket.name}.")


# [END storage_set_public_access_prevention_inherited]

if __name__ == "__main__":
    set_public_access_prevention_inherited(bucket_name=sys.argv[1])
