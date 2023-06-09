#!/usr/bin/env python

# Copyright 2016 Google LLC
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

"""Example of authenticating using Application Default Credentials on
Compute Engine.

For more information, see the README.md under /compute.
"""

# [START compute_auth_application_default]
import argparse
from typing import List

from google.cloud import storage


def create_client() -> storage.Client:
    """
    Construct a client object for the Storage API using the
    application default credentials.

    Returns:
        Storage API client object.
    """
    # Construct the service object for interacting with the Cloud Storage API -
    # the 'storage' service, at version 'v1'.
    # Authentication is provided by application default credentials.
    # When running locally, these are available after running
    # `gcloud auth application-default login`. When running on Compute
    # Engine, these are available from the environment.
    return storage.Client()


def list_buckets(client: storage.Client, project_id: str) -> List[storage.Bucket]:
    """
    Retrieve bucket list of a project using provided client object.


    Args:
        client: Storage API client object.
        project_id: name of the project to list buckets from.

    Returns:
        List of Buckets found in the project.
    """
    buckets = client.list_buckets()
    return list(buckets)


def main(project_id: str) -> None:
    client = create_client()
    buckets = list_buckets(client, project_id)
    print(buckets)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Your Google Cloud Project ID.")

    args = parser.parse_args()

    main(args.project_id)
# [END compute_auth_application_default]
