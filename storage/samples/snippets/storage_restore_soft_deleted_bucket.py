#!/usr/bin/env python

# Copyright 2025 Google LLC
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

# [START storage_restore_soft_deleted_bucket]

from google.cloud import storage


def restore_bucket(bucket_name, bucket_generation):
    storage_client = storage.Client()
    bucket = storage_client.restore_bucket(bucket_name=bucket_name, generation=bucket_generation)
    print(f"Soft-deleted bucket {bucket.name} with ID: {bucket.id} was restored.")
    print(f"Bucket Generation: {bucket.generation}")


# [END storage_restore_soft_deleted_bucket]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong inputs!! Usage of script - \"python storage_restore_soft_deleted_bucket.py <bucket_name> <bucket_generation>\" ")
        sys.exit(1)
    restore_bucket(bucket_name=sys.argv[1], bucket_generation=sys.argv[2])
