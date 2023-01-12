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
"""
command line application and sample code for deleting an existing secret.
"""

import argparse


# [START secretmanager_delete_secret_with_etag]
def delete_secret_with_etag(project_id, secret_id, etag):
    """
    Delete the secret with the given name, etag, and all of its versions.
    """

    # Import the Secret Manager client library and types.
    from google.cloud import secretmanager
    from google.cloud.secretmanager_v1.types import service

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = client.secret_path(project_id, secret_id)

    # Build the request
    request = service.DeleteSecretRequest()
    request.name = name
    request.etag = etag

    # Delete the secret.
    client.delete_secret(request=request)


# [END secretmanager_delete_secret_with_etag]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to delete")
    parser.add_argument("etag", help="current etag of the secret to delete")
    args = parser.parse_args()

    delete_secret_with_etag(args.project_id, args.secret_id, args.etag)
