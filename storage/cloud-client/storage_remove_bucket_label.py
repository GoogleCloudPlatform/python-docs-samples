#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
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


# [START storage_remove_bucket_label]
import pprint
# [END storage_remove_bucket_label]
import sys
# [START storage_remove_bucket_label]

from google.cloud import storage


def remove_bucket_label(bucket_name):
    """Remove a label from a bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    labels = bucket.labels

    if "example" in labels:
        del labels["example"]

    bucket.labels = labels
    bucket.patch()

    print("Removed labels on {}.".format(bucket.name))
    pprint.pprint(bucket.labels)


# [END storage_remove_bucket_label]

if __name__ == "__main__":
    remove_bucket_label(bucket_name=sys.argv[1])
