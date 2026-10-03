#!/usr/bin/env python

# Copyright 2026 Google LLC
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
command line application and sample code for enabling managed rotation of
a Cloud SQL DB credentials secret.
"""

# [START secretmanager_enable_regional_secret_managed_rotation]
import argparse

# Import the Secret Manager client library.
from google.cloud import secretmanager_v1


def enable_regional_secret_managed_rotation(
    project_id: str,
    location_id: str,
    secret_id: str,
    instance_id: str,
    username: str,
) -> secretmanager_v1.SecretVersion:
    """
    Enable managed rotation for a Cloud SQL DB credentials secret. This
    links the secret to a Cloud SQL instance and database user, and can
    only be called once per secret. It adds the secret's first version and
    sets the matching password on the Cloud SQL user, taking the place of
    a manually added secret version, which this secret type doesn't
    support. Afterwards, use rotate_regional_secret.py to trigger further
    rotations.

    instance_id is the bare Cloud SQL instance ID (e.g. "my-instance") --
    not a connection name. Neither the project nor the region should be
    included: passing "PROJECT_ID:INSTANCE_ID" (as gcloud's own
    `enable-managed-rotation --help` examples misleadingly show) or the
    full "PROJECT_ID:LOCATION_ID:INSTANCE_ID" connection name both fail --
    the service already knows the project from the secret's own path, and
    prepends it internally, so a qualified value ends up double-prefixed.
    """

    # Endpoint to call the regional Secret Manager API.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the secret.
    parent = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"

    # Enable managed rotation. Leaving password unset lets Secret Manager
    # generate a secure password itself.
    response = client.enable_managed_rotation(
        request={
            "parent": parent,
            "cloud_sql_single_user_credentials": {
                "instance_id": instance_id,
                "username": username,
            },
        }
    )

    print(f"Enabled managed rotation, created secret version: {response.name}")

    return response


# [END secretmanager_enable_regional_secret_managed_rotation]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of location where secret is stored")
    parser.add_argument(
        "secret_id",
        help="id of the Cloud SQL DB credentials secret to enable rotation on",
    )
    parser.add_argument(
        "instance_id",
        help="bare id of the Cloud SQL instance (no project or region prefix)",
    )
    parser.add_argument("username", help="username of the Cloud SQL database user")
    args = parser.parse_args()

    enable_regional_secret_managed_rotation(
        args.project_id,
        args.location_id,
        args.secret_id,
        args.instance_id,
        args.username,
    )
