#!/usr/bin/env python

# Copyright 2021 Google LLC. All Rights Reserved.
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

"""Sample that configures retries on an operation call.
This sample is used on this page:
    https://cloud.google.com/storage/docs/retry-strategy
For more information, see README.md.
"""

# [START storage_configure_retries]
from google.cloud import storage
from google.cloud.storage.retry import DEFAULT_RETRY


def configure_retries(bucket_name, blob_name):
    """Configures retries with customizations."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # blob_name = "your-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Customize retry with a deadline of 500 seconds (default=120 seconds).
    modified_retry = DEFAULT_RETRY.with_deadline(500.0)
    # Customize retry with an initial wait time of 1.5 (default=1.0).
    # Customize retry with a wait time multiplier per iteration of 1.2 (default=2.0).
    # Customize retry with a maximum wait time of 45.0 (default=60.0).
    modified_retry = modified_retry.with_delay(initial=1.5, multiplier=1.2, maximum=45.0)

    # blob.delete() uses DEFAULT_RETRY_IF_GENERATION_SPECIFIED by default.
    # Override with modified_retry so the function retries even if the generation
    # number is not specified.
    print(
        f"The following library method is customized to be retried according to the following configurations: {modified_retry}"
    )

    blob.delete(retry=modified_retry)
    print("Blob {} deleted with a customized retry strategy.".format(blob_name))


# [END storage_configure_retries]


if __name__ == "__main__":
    configure_retries(bucket_name=sys.argv[1], blob_name=sys.argv[2])
