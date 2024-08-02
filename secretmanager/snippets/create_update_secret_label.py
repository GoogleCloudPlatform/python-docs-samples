#!/usr/bin/env python

# Copyright 2024 Google LLC
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

# [START secretmanager_create_update_secret_label]

import argparse
from typing import Dict

# Import the Secret Manager client library.
from google.cloud import secretmanager


def create_update_secret_label(
    project_id: str, secret_id: str, new_labels: Dict[str, str]
) -> secretmanager.UpdateSecretRequest:
    """
    Create or update a label on an existing secret.
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = client.secret_path(project_id, secret_id)

    # Get the secret.
    response = client.get_secret(request={"name": name})

    labels = response.labels

    # Update the labels
    for label_key in new_labels:
        labels[label_key] = new_labels[label_key]

    # Update the secret.
    secret = {"name": name, "labels": labels}
    update_mask = {"paths": ["labels"]}
    response = client.update_secret(
        request={"secret": secret, "update_mask": update_mask}
    )

    # Print the new secret name.
    print(f"Updated secret: {response.name}")

    return response


# [END secretmanager_create_update_secret_label]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to act on")
    parser.add_argument("label_key", help="key of the label to be added/updated")
    parser.add_argument("label_value", help="value of the label to be added/updated")
    args = parser.parse_args()

    labels = {args.label_key, args.label_value}
    create_update_secret_label(args.project_id, args.secret_id, labels)
