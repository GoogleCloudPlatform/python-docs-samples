#!/usr/bin/env python

# Copyright 2024 Google LLC
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

# [START storage_create_bucket_hierarchical_namespace]
from google.cloud import storage


def create_bucket_hierarchical_namespace(bucket_name):
    """Creates a bucket with hierarchical namespace enabled."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.hierarchical_namespace_enabled = True
    bucket.create()

    print(f"Created bucket {bucket_name} with hierarchical namespace enabled.")


# [END storage_create_bucket_hierarchical_namespace]


if __name__ == "__main__":
    create_bucket_hierarchical_namespace(bucket_name=sys.argv[1])
