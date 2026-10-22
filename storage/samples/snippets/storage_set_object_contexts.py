#!/usr/bin/env python

# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

# [START storage_set_object_contexts]
from google.cloud import storage
from google.cloud.storage.blob import ObjectCustomContextPayload


def set_object_contexts(bucket_name, blob_name):
    """Sets, updates and deletes custom contexts on an object."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # blob_name = "your-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)

    # Optional: set a metageneration-match precondition to avoid potential race
    # conditions and data corruptions. The request to patch is aborted if the
    # object's metageneration does not match your precondition.
    metageneration_match_precondition = blob.metageneration

    contexts = blob.contexts
    # Add or update the values of custom contexts.
    contexts.custom["key1"] = ObjectCustomContextPayload(value="newValue1")
    contexts.custom["key3"] = ObjectCustomContextPayload(value="value3")
    # Setting a context's value to None deletes that key from the object.
    contexts.custom["key2"] = ObjectCustomContextPayload(value=None)
    # Reassign the contexts so the change is tracked for the patch request.
    blob.contexts = contexts
    blob.patch(if_metageneration_match=metageneration_match_precondition)

    print(f"Updated contexts for {blob.name}:")
    for key, payload in blob.contexts.custom.items():
        print(f"{key} = {payload.value}")


# [END storage_set_object_contexts]

if __name__ == "__main__":
    set_object_contexts(bucket_name=sys.argv[1], blob_name=sys.argv[2])
