# Copyright 2018 Google LLC All Rights Reserved.
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

import argparse
import os

from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def get_client(service_account_json):
    """Returns an authorized API client by discovering the Healthcare API and
    creating a service object using the service account credentials JSON."""
    api_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    api_version = "v1beta1"
    discovery_api = "https://healthcare.googleapis.com/$discovery/rest"
    service_name = "healthcare"

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json
    )
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = f"{discovery_api}?labels=CHC_BETA&version={api_version}"

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials,
    )


def create_dataset(service_account_json, project_id, cloud_region, dataset_id):
    """Creates a dataset."""
    client = get_client(service_account_json)
    dataset_parent = f"projects/{project_id}/locations/{cloud_region}"

    body = {}

    request = (
        client.projects()
        .locations()
        .datasets()
        .create(parent=dataset_parent, body=body, datasetId=dataset_id)
    )

    try:
        response = request.execute()
        print(f"Created dataset: {dataset_id}")
        return response
    except HttpError as e:
        print(f"Error, dataset not created: {e}")
        return ""


def delete_dataset(service_account_json, project_id, cloud_region, dataset_id):
    """Deletes a dataset."""
    client = get_client(service_account_json)
    dataset_name = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )

    request = client.projects().locations().datasets().delete(name=dataset_name)

    try:
        response = request.execute()
        print(f"Deleted dataset: {dataset_id}")
        return response
    except HttpError as e:
        print(f"Error, dataset not deleted: {e}")
        return ""


def create_fhir_store(
    service_account_json, project_id, cloud_region, dataset_id, fhir_store_id
):
    """Creates a new FHIR store within the parent dataset."""
    client = get_client(service_account_json)
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )

    body = {"version": "R4"}

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .create(parent=fhir_store_parent, body=body, fhirStoreId=fhir_store_id)
    )

    response = request.execute()
    print(f"Created FHIR store: {fhir_store_id}")
    return response


def delete_fhir_store(
    service_account_json, project_id, cloud_region, dataset_id, fhir_store_id
):
    """Deletes the specified FHIR store."""
    client = get_client(service_account_json)
    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )
    fhir_store_name = f"{fhir_store_parent}/fhirStores/{fhir_store_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .delete(name=fhir_store_name)
    )

    response = request.execute()
    print(f"Deleted FHIR store: {fhir_store_id}")
    return response


def parse_command_line_args():
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--service_account_json",
        default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        help="Path to service account JSON file.",
    )

    parser.add_argument(
        "--project_id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help="GCP cloud project name",
    )

    parser.add_argument(
        "--cloud_region", default="us-central1", help="GCP cloud region"
    )

    parser.add_argument("--dataset_id", default=None, help="Name of dataset")

    parser.add_argument("--fhir_store_id", default=None, help="Name of FHIR store")

    command = parser.add_subparsers(dest="command")

    command.add_parser("create-dataset", help=create_dataset.__doc__)
    command.add_parser("delete-dataset", help=delete_dataset.__doc__)
    command.add_parser("create-fhir-store", help=create_fhir_store.__doc__)
    command.add_parser("delete-fhir-store", help=delete_fhir_store.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print(
            "You must specify a project ID or set the "
            '"GOOGLE_CLOUD_PROJECT" environment variable.'
        )
        return

    elif args.command == "create-dataset":
        create_fhir_store(
            args.service_account_json,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
        )

    elif args.command == "delete-dataset":
        create_fhir_store(
            args.service_account_json,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
        )

    elif args.command == "create-fhir-store":
        create_fhir_store(
            args.service_account_json,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
        )

    elif args.command == "delete-fhir-store":
        delete_fhir_store(
            args.service_account_json,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
