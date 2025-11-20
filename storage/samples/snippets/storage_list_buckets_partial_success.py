#!/usr/bin/env python

# Copyright 2025 Google Inc. All Rights Reserved.
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

# [START storage_list_buckets_partial_success]
from google.cloud import storage


def list_buckets_with_partial_success():
    """Lists buckets and includes unreachable buckets in the response."""

    storage_client = storage.Client()

    buckets_iterator = storage_client.list_buckets(return_partial_success=True)

    for page in buckets_iterator.pages:
        if page.unreachable:
            print("Unreachable locations in this page:")
            for location in page.unreachable:
                print(location)

        print("Reachable buckets in this page:")
        for bucket in page:
            print(bucket.name)


# [END storage_list_buckets_partial_success]


if __name__ == "__main__":
    list_buckets_with_partial_success()
