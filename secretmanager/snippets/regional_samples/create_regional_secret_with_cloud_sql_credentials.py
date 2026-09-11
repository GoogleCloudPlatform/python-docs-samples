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
command line application and sample code for creating a new secret that is
eligible for Cloud SQL managed rotation.
"""

# [START secretmanager_create_regional_secret_with_cloud_sql_credentials]
import argparse

# Import the Secret Manager client library.
from google.cloud import secretmanager_v1


def create_regional_secret_with_cloud_sql_credentials(
    project_id: str,
    location_id: str,
    secret_id: str,
) -> secretmanager_v1.Secret:
    """
    Create a new secret with the Cloud SQL DB credentials secret type. This
    type is required to enable Secret Manager's automatic rotation of Cloud
    SQL passwords. It can only be set when the secret is created, and the
    secret's location must match the region of the target Cloud SQL
    instance.
    """

    # Endpoint to call the regional Secret Manager API.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}/locations/{location_id}"

    # Create the secret.
    response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "secret_type": secretmanager_v1.Secret.SecretType.CLOUD_SQL_DB_CREDENTIALS,
            },
        }
    )

    # Print the new secret name.
    print(f"Created secret: {response.name}")

    # This built-in identity is what you grant Cloud SQL IAM permissions to,
    # so that Secret Manager can rotate the database password on its behalf.
    print(
        "Grant this identity Cloud SQL IAM permissions to enable rotation: "
        f"{response.policy_member.iam_policy_uid_principal}"
    )

    return response


# [END secretmanager_create_regional_secret_with_cloud_sql_credentials]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument(
        "location_id",
        help="id of the location where secret is to be created; must match "
        "the Cloud SQL instance's region",
    )
    parser.add_argument("secret_id", help="id of the secret to create")
    args = parser.parse_args()

    create_regional_secret_with_cloud_sql_credentials(
        args.project_id, args.location_id, args.secret_id
    )
