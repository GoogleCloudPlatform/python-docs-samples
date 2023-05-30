#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
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

# [START all]

import argparse
from typing import Dict

import googleapiclient.discovery


def create_service() -> googleapiclient.discovery.Resource:
    """Construct the service object for interacting with the Cloud Storage API -
    the 'storage' service, at version 'v1'.
    Authentication is provided by application default credentials.
    When running locally, these are available after running
    `gcloud auth application-default login`. When running on Compute Engine,
    these are available from the environment."""
    return googleapiclient.discovery.build("storage", "v1")


def list_buckets(service: googleapiclient.discovery.Resource, project_id: str) -> Dict:
    """List buckets in Cloud Storage"""
    return service.buckets().list(project=project_id).execute()


def main(project_id: str) -> None:
    service = create_service()
    buckets = list_buckets(service, project_id)
    print(buckets)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Your Google Cloud Project ID.")

    args = parser.parse_args()

    main(args.project_id)
# [END all]
