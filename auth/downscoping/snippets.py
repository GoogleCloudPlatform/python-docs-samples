#!/usr/bin/env python

# Copyright 2021 Google LLC
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

"""Demonstrates how to use Downscoping with Credential Access Boundaries."""

# [START auth_downscoping_token_broker]
import google.auth

from google.auth import downscoped
from google.auth.transport import requests

# [END auth_downscoping_token_broker]
# [START auth_downscoping_token_consumer]
from google.cloud import storage
from google.oauth2 import credentials

# [END auth_downscoping_token_consumer]


# [START auth_downscoping_token_broker]
def get_token_from_broker(bucket_name, object_prefix):
    """Simulates token broker generating downscoped tokens for specified bucket.

    Args:
        bucket_name (str): The name of the Cloud Storage bucket.
        object_prefix (str): The prefix string of the object name. This is used
            to ensure access is restricted to only objects starting with this
            prefix string.

    Returns:
        Tuple[str, datetime.datetime]: The downscoped access token and its expiry date.
    """
    # [START auth_downscoping_rules]
    # Initialize the Credential Access Boundary rules.
    available_resource = f"//storage.googleapis.com/projects/_/buckets/{bucket_name}"
    # Downscoped credentials will have readonly access to the resource.
    available_permissions = ["inRole:roles/storage.objectViewer"]
    # Only objects starting with the specified prefix string in the object name
    # will be allowed read access.
    availability_expression = (
        "resource.name.startsWith('projects/_/buckets/{}/objects/{}')".format(
            bucket_name, object_prefix
        )
    )
    availability_condition = downscoped.AvailabilityCondition(availability_expression)
    # Define the single access boundary rule using the above properties.
    rule = downscoped.AccessBoundaryRule(
        available_resource=available_resource,
        available_permissions=available_permissions,
        availability_condition=availability_condition,
    )
    # Define the Credential Access Boundary with all the relevant rules.
    credential_access_boundary = downscoped.CredentialAccessBoundary(rules=[rule])
    # [END auth_downscoping_rules]

    # [START auth_downscoping_initialize_downscoped_cred]
    # Retrieve the source credentials via ADC.
    source_credentials, _ = google.auth.default()
    if source_credentials.requires_scopes:
        source_credentials = source_credentials.with_scopes(
            ["https://www.googleapis.com/auth/cloud-platform"]
        )

    # Create the downscoped credentials.
    downscoped_credentials = downscoped.Credentials(
        source_credentials=source_credentials,
        credential_access_boundary=credential_access_boundary,
    )

    # Refresh the tokens.
    downscoped_credentials.refresh(requests.Request())

    # These values will need to be passed to the token consumer.
    access_token = downscoped_credentials.token
    expiry = downscoped_credentials.expiry
    # [END auth_downscoping_initialize_downscoped_cred]
    return (access_token, expiry)


# [END auth_downscoping_token_broker]


# [START auth_downscoping_token_consumer]
def token_consumer(bucket_name, object_name):
    """Tests token consumer readonly access to the specified object.

    Args:
        bucket_name (str): The name of the Cloud Storage bucket.
        object_name (str): The name of the object in the Cloud Storage bucket
            to read.
    """
    # Create the OAuth credentials from the downscoped token and pass a
    # refresh handler to handle token expiration. We are passing a
    # refresh_handler instead of a one-time access token/expiry pair.
    # This will allow the consumer to obtain new downscoped tokens on
    # demand every time a token is expired, without any additional code
    # changes.
    def refresh_handler(request, scopes=None):
        # The common pattern of usage is to have a token broker pass the
        # downscoped short-lived access tokens to a token consumer via some
        # secure authenticated channel.
        # For illustration purposes, we are generating the downscoped token
        # locally.
        # We want to test the ability to limit access to objects with a certain
        # prefix string in the resource bucket. object_name[0:3] is the prefix
        # here. This field is not required if access to all bucket resources are
        # allowed. If access to limited resources in the bucket is needed, this
        # mechanism can be used.
        return get_token_from_broker(bucket_name, object_prefix=object_name[0:3])

    creds = credentials.Credentials(
        None,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
        refresh_handler=refresh_handler,
    )

    # Initialize a Cloud Storage client with the oauth2 credentials.
    storage_client = storage.Client(credentials=creds)
    # The token broker has readonly access to the specified bucket object.
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    print(blob.download_as_bytes().decode("utf-8"))


# [END auth_downscoping_token_consumer]


def main(bucket_name, object_name):
    """The main function used to test downscoping functionality.

    This will generate downscope tokens (readonly access), inject them
    into a storage instance and then test readonly access.

    Args:
        bucket_name (str): The name of the Cloud Storage bucket.
        object_name (str): The name of the object in the bucket.
    """
    # Storage client using ADC.
    print("Testing token consumer read access...")
    token_consumer(bucket_name, object_name)
    print("Done")
