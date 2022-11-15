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
command line application and sample code for listing secrets in a project.
"""


# [START secretmanager_list_secrets_with_filter]
def list_secrets_with_filter(project_id, filter_str):
    """
    List all secrets in the given project.

    Args:
      project_id: Parent project id
      filter_str: Secret filter, constructing according to
                  https://cloud.google.com/secret-manager/docs/filtering
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}"

    # List all secrets.
    for secret in client.list_secrets(request={"parent": parent, "filter": filter_str}):
        print("Found secret: {}".format(secret.name))


# [END secretmanager_list_secrets_with_filter]
