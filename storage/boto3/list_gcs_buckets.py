#!/usr/bin/env python

# [START gcs_boto3_list_buckets]
# Use GCS XML API with the AWS boto3 SDK
# Import the boto3 SDK.
import boto3

def list_gcs_buckets(
        google_access_key_id='ACCESS_KEY',
        google_secret_access_key='SECRET_KEY'):
    """Lists all buckets using boto3 SDK"""
    # Create an S3 client to interact with GCS XML API
    # 1. Change endpoint URL to the GCS XML API endpoint URL.
    # 2. Use GCS HMAC interoperable credentials.
    s3 = boto3.client('s3',
        endpoint_url="https://storage.googleapis.com",
        aws_access_key_id=google_access_key_id,
        aws_secret_access_key=google_secret_access_key)

    # Call GCS to list current buckets
    response = s3.list_buckets()

    # Print bucket names
    for bucket in response["Buckets"]:
        print(bucket["Name"])
# [END gcs_boto3_list_buckets]


if __name__ == '__main__':
    list_gcs_buckets(
        google_access_key_id=sys.argv[1],
        google_secret_access_key=sys.argv[2])
