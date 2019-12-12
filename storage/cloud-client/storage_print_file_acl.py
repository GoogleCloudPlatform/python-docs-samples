#!/usr/bin/env python

# Copyright 2019 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

# [START storage_print_file_acl]
from google.cloud import storage


def print_blob_acl(bucket_name, blob_name):
    """Prints out a blob's access control list."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    for entry in blob.acl:
        print("{}: {}".format(entry["role"], entry["entity"]))


# [END storage_print_file_acl]

if __name__ == "__main__":
    print_blob_acl(bucket_name=sys.argv[1], blob_name=sys.argv[2])
