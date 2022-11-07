#!/usr/bin/env python

# Copyright 2022 Google LLC
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

# [START storage_set_autoclass]
from google.cloud import storage


def set_autoclass(bucket_name, toggle):
    """Disable Autoclass for a bucket.

    Note: Only patch requests that disable autoclass are currently supported.
    To enable autoclass, you must set it at bucket creation time.
    """
    # The ID of your GCS bucket
    # bucket_name = "my-bucket"
    # Boolean toggle - if true, enables Autoclass; if false, disables Autoclass
    # toggle = False

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.autoclass_enabled = toggle
    bucket.patch()
    print(f"Autoclass enabled is set to {bucket.autoclass_enabled} for {bucket.name} at {bucket.autoclass_toggle_time}.")

    return bucket


# [END storage_set_autoclass]

if __name__ == "__main__":
    set_autoclass(bucket_name=sys.argv[1], toggle=sys.argv[2])
