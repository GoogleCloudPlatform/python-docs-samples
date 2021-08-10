# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demonstrates how to use Downscoping with Credential Access Boundaries."""

import google.auth

from google.auth import downscoped
from google.auth.transport import requests
from google.cloud import storage

import google.oauth2


OBJECT_PREFIX_NAME = "customer-a"


# [START auth_downscoping_token_broker]
def get_token_from_broker(bucket_name, object_prefix):
    """Simulates token broker generating downscoped tokens for specified bucket.

    Args:
        bucket_name (str): The name of the cloud storage bucket.
        object_prefix (str): The prefix string of the object blob name. This is used
            to ensure access is restricted to only objects starting with this
            prefix string.

    Returns:
        Tuple[str, datetime]: The downscoped access token and its expiry date.
    """
    # [START auth_downscoping_rules]
    # Initialize the credential access boundary rules.
    available_resource = f"//storage.googleapis.com/projects/_/buckets/{bucket_name}"
    # Downscoped credentials will have readonly access to the resource.
    available_permissions = ["inRole:roles/storage.objectViewer"]
    availability_expression = (
        "resource.name.startsWith('projects/_/buckets/{}/objects/{}')".format(
            bucket_name, object_prefix
        )
    )

    availability_condition = downscoped.AvailabilityCondition(availability_expression)
    rule = downscoped.AccessBoundaryRule(
        available_resource=available_resource,
        available_permissions=available_permissions,
        availability_condition=availability_condition,
    )
    credential_access_boundary = downscoped.CredentialAccessBoundary(rules=[rule])
    # [END auth_downscoping_rules]

    # [START auth_downscoping_initialize_downscoped_cred]
    # Retrieve the source credentials via ADC.
    source_credentials, _ = google.auth.default()

    # Create the downscoped credentials.
    downscoped_credentials = downscoped.Credentials(
        source_credentials=source_credentials,
        credential_access_boundary=credential_access_boundary,
    )

    # Refresh the tokens.
    downscoped_credentials.refresh(requests.Request())

    # These values will need to be passed to the Token Consumer.
    access_token = downscoped_credentials.token
    expiry = downscoped_credentials.expiry
    # [END auth_downscoping_initialize_downscoped_cred]
    return (access_token, expiry)


# [END auth_downscoping_token_broker]


# [START auth_downscoping_token_consumer]
def token_consumer(bucket_name, object_name):
    """Tests token consumer readonly access to the specified object.

    Args:
        bucket_name (str): The name of the cloud storage bucket.
        object_name (str): The name of the object in the storage bucket to
            read.
    """
    # Create the OAuth credentials from the downscoped token and pass a
    # refresh handler to handle token expiration. Passing the original
    # downscoped token or the expiry here is optional, as the refresh_handler
    # will generate the downscoped token on demand.
    def refresh_handler(request, scopes=None):
        # The common pattern of usage is to have a token broker pass the
        # downscoped short-lived access tokens to a token consumer via some
        # secure authenticated channel.
        # For illustration purposes, we are generating the downscoped token
        # locally.
        return get_token_from_broker(bucket_name, OBJECT_PREFIX_NAME)

    credentials = google.oauth2.credentials.Credentials(
        None,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
        refresh_handler=refresh_handler,
    )

    # Initialize a storage client with the oauth2 credentials.
    storage_client = storage.Client(credentials=credentials)
    # The token broker has readonly access to the specified bucket object.
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    print(blob.download_as_bytes().decode("utf-8"))


# [END auth_downscoping_token_consumer]


def upload_object(storage_client, bucket_name, source_file_name, destination_blob_name):
    """Upload object from source file to specified object under blob name.

    By default the object is created as non-public.

    Args:
        storage_client (google.cloud.storage.Client): The storage client
            instance.
        bucket_name (str): The name of the cloud storage bucket.
        source_file_name (str): The file path to the source file to upload.
        destination_blob_name (str): The object name under which the file will
            be uploaded.
    """
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def delete_object(storage_client, bucket_name, blob_name):
    """Delete object of blob name under specified bucket.

    Args:
        storage_client (google.cloud.storage.Client): The storage client
            instance.
        bucket_name (str): The name of the cloud storage bucket.
        blob_name (str): The object name in the storage bucket to be deleted.
    """
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()


def main(bucket_name, filename):
    """The main function used to test downscoping functionality.

    This will upload the file to the storage bucket, generate downscoped
    tokens (readonly access), inject them into a storage instance and then
    test readonly access. On completion, the object will be deleted.

    Args:
        bucket_name (str): The name of the cloud storage bucket.
        filename (str): The file path to the source file to upload.
    """
    # Storage client using ADC.
    storage_client = storage.Client()
    try:
        # The name of the test object to be accessed in the bucket.
        blob_name = f"{OBJECT_PREFIX_NAME}-data.txt"
        print("Uploading object...")
        upload_object(storage_client, bucket_name, filename, blob_name)

        print("Testing token consumer read access...")
        token_consumer(bucket_name, blob_name)
    finally:
        print("Deleting object...")
        delete_object(storage_client, bucket_name, blob_name)
    print("Done")
