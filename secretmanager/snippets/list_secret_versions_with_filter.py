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
command line application and sample code for listing secret versions of a
secret.
"""


# [START secretmanager_list_secret_versions_with_filter]
def list_secret_versions_with_filter(project_id, secret_id, filter_str="state:ENABLED"):
    """
    List all secret versions in the given secret and their metadata.

    Args:
      project_id: Parent project id
      secret_id: Parent secret id
      filter_str: Secret version filter, constructing according to
                  https://cloud.google.com/secret-manager/docs/filtering
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent secret.
    parent = client.secret_path(project_id, secret_id)

    # List all secret versions.
    for version in client.list_secret_versions(
        request={"parent": parent, "filter": filter_str}
    ):
        print(f"Found secret version: {version.name}")


# [END secretmanager_list_secret_versions_with_filter]
