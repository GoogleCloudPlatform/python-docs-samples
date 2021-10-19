#!/usr/bin/env python

# Copyright 2020 Google Inc. All Rights Reserved.
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

# [START storage_disable_versioning]
from google.cloud import storage


def disable_versioning(bucket_name):
    """Disable versioning for this bucket."""
    # bucket_name = "my-bucket"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.versioning_enabled = False
    bucket.patch()

    print("Versioning was disabled for bucket {}".format(bucket))
    return bucket


# [END storage_disable_versioning]

if __name__ == "__main__":
    disable_versioning(bucket_name=sys.argv[1])
