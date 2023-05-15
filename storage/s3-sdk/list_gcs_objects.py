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

# [START storage_s3_sdk_list_objects]
import boto3  # type: ignore


def list_gcs_objects(
    google_access_key_id: str, google_access_key_secret: str, bucket_name: str
) -> None:
    """Lists GCS objects using boto3 SDK"""
    # Create a new client and do the following:
    # 1. Change the endpoint URL to use the
    #    Google Cloud Storage XML API endpoint.
    # 2. Use Cloud Storage HMAC Credentials.

    client = boto3.client(
        "s3",
        region_name="auto",
        endpoint_url="https://storage.googleapis.com",
        aws_access_key_id=google_access_key_id,
        aws_secret_access_key=google_access_key_secret,
    )

    # Call GCS to list objects in bucket_name
    response = client.list_objects(Bucket=bucket_name)

    # Print object names
    print("Objects:")
    for blob in response["Contents"]:
        print(blob["Key"])


# [END storage_s3_sdk_list_objects]


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
    parser.add_argument("bucket_name", help="Your Cloud Storage bucket name")

    args = parser.parse_args()

    list_gcs_objects(
        google_access_key_id=args.google_access_key_id,
        google_access_key_secret=args.google_access_key_secret,
        bucket_name=args.bucket_name,
    )
