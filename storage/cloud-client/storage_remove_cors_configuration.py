#!/usr/bin/env python

# Copyright 2020 Google LLC. All Rights Reserved.
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

# [START storage_remove_cors_configuration]
from google.cloud import storage


def remove_cors_configuration(bucket_name):
    """Remove a bucket's CORS policies configuration."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.cors = []
    bucket.patch()

    print("Remove CORS policies for bucket {}.".format(bucket.name))
    return bucket


# [END storage_remove_cors_configuration]

if __name__ == "__main__":
    remove_cors_configuration(bucket_name=sys.argv[1])
