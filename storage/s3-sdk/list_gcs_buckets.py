#!/usr/bin/env python

# Copyright 2018 Google, Inc.
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

"""This sample shows how to list Google Cloud Storage (GCS) buckets
   using the AWS S3 SDK with the GCS interoperable XML API.

GCS Credentials are passed in using the following environment variables:

    * AWS_ACCESS_KEY_ID
    * AWS_SECRET_ACCESS_KEY

Learn how to get GCS interoperable credentials at
https://cloud.google.com/storage/docs/migrating#keys.
"""

# [START gcs_s3_sdk_list_buckets]
import boto3


def list_gcs_buckets():
    """Lists all GCS buckets using boto3 SDK"""
    # Change the endpoint_url to use the Google Cloud Storage XML API endpoint.
    s3 = boto3.client('s3', region_name="auto",
                      endpoint_url="https://storage.googleapis.com")

    # Call GCS to list current buckets
    response = s3.list_buckets()

    # Print bucket names
    print("Buckets:")
    for bucket in response["Buckets"]:
        print(bucket["Name"])
# [END gcs_s3_sdk_list_buckets]


if __name__ == '__main__':
    list_gcs_buckets()
