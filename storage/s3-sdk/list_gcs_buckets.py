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

import argparse

# [START storage_s3_sdk_list_buckets]
import boto3  # type: ignore


def list_gcs_buckets(
    google_access_key_id: str, google_access_key_secret: str
) -> list[str]:
    """Lists all Cloud Storage buckets using AWS SDK for Python (boto3)
    Positional arguments:
        google_access_key_id: hash-based message authentication code (HMAC) access ID
        google_access_key_secret: HMAC access secret

    Returned value is a list of strings, one for each bucket name.

    To use this sample:
    1. Create a Cloud Storage HMAC key: https://cloud.google.com/storage/docs/authentication/managing-hmackeys#create
    2. Change endpoint_url to a Google Cloud Storage XML API endpoint.

    To learn more about HMAC: https://cloud.google.com/storage/docs/authentication/hmackeys#overview
    """
    client = boto3.client(
        "s3",
        region_name="auto",
        endpoint_url="https://storage.googleapis.com",
        aws_access_key_id=google_access_key_id,
        aws_secret_access_key=google_access_key_secret,
    )

    # Call GCS to list current buckets
    response = client.list_buckets()

    # Return list of bucket names
    results = []
    for bucket in response["Buckets"]:
        results.append(bucket["Name"])
        print(bucket["Name"])  # Can remove if not needed after development
    return results
# [END storage_s3_sdk_list_buckets]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "google_access_key_id", help="Your Cloud Storage HMAC Access Key ID."
    )
    parser.add_argument(
        "google_access_key_secret", help="Your Cloud Storage HMAC Access Key Secret."
    )

    args = parser.parse_args()

    list_gcs_buckets(
        google_access_key_id=args.google_access_key_id,
        google_access_key_secret=args.google_access_key_secret,
    )
