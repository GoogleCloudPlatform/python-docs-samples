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
import json
import os
import httplib2
import google.auth

from googleapiclient import discovery
from google.oauth2 import service_account
from googleapiclient.http import build_http
from oauth2client.service_account import ServiceAccountCredentials

# [START healthcare_get_client]
def get_client():
    """Returns an authorized API client by discovering the Healthcare API and
    creating a service object using the service account credentials in the
    GOOGLE_APPLICATION_CREDENTIALS environment variable."""
    api_version = "v1"
    service_name = "healthcare"

    return discovery.build(service_name, api_version)


# [END healthcare_get_client]


# [START healthcare_get_client_fhir]
def get_client_fhir():
    """Returns an authorized API client by discovering the Healthcare API and
    creating a service object using the service account credentials in the
    GOOGLE_APPLICATION_CREDENTIALS environment variable. Many FHIR resource
    requests require a custom HTTP header to be set, so we have to override
    the httplib2.Http object.
    """
    credential_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credential_path, scopes
    )
    http = httplib2.Http()
    http = credentials.authorize(http=build_http())
    http.headers = {"Content-Type": "application/fhir+json;charset=utf-8"}
    return discovery.build("healthcare", "v1", http=http)


# [END healthcare_get_client_fhir]


# [START healthcare_create_resource]
def create_patient(project_id, cloud_region, dataset_id, fhir_store_id):
    """Creates a new Patient resource in a FHIR store."""
    client = get_client_fhir()

    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )

    fhir_store_name = "{}/fhirStores/{}".format(fhir_store_parent, fhir_store_id)

    resource_type = "Patient"

    body = {
        "name": [{"use": "official", "family": "Smith", "given": ["Darcy"]}],
        "gender": "female",
        "birthDate": "1970-01-01",
        "resourceType": "{}".format(resource_type),
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .create(parent=fhir_store_name, type=resource_type, body=body)
    )
    response = request.execute()

    print("Created Patient resource with ID {}".format(response["id"]))
    print(json.dumps(response, indent=2))

    return response


# [END healthcare_create_resource]


# [START healthcare_create_encounter]
def create_encounter(
    project_id, cloud_region, dataset_id, fhir_store_id, patient_id,
):
    """Creates a new Encounter resource in a FHIR store based on a Patient."""
    client = get_client_fhir()

    fhir_store_name = "projects/{}/locations/{}/datasets/{}/fhirStores/{}".format(
        project_id, cloud_region, dataset_id, fhir_store_id
    )

    resource_type = "Encounter"

    body = {
        "status": "finished",
        "class": {
            "system": "http://hl7.org/fhir/v3/ActCode",
            "code": "IMP",
            "display": "inpatient encounter",
        },
        "reason": [
            {
                "text": "The patient had an abnormal heart rate. She was"
                " concerned about this."
            }
        ],
        "subject": {"reference": "Patient/{}".format(patient_id)},
        "resourceType": "Encounter",
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .create(parent=fhir_store_name, type=resource_type, body=body)
    )
    response = request.execute()

    print("Created Encounter resource with ID {}".format(response["id"]))
    print(json.dumps(response, indent=2))


# [END healthcare_create_encounter]


# [START healthcare_delete_resource]
def delete_resource(
    project_id, cloud_region, dataset_id, fhir_store_id, resource_type, resource_id,
):
    """
    Deletes a FHIR resource. Regardless of whether the operation succeeds or
    fails, the server returns a 200 OK HTTP status code. To check that the
    resource was successfully deleted, search for or get the resource and
    see if it exists.
    """
    client = get_client()

    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )

    resource_name = "{}/fhirStores/{}/fhir/{}/{}".format(
        fhir_store_parent, fhir_store_id, resource_type, resource_id
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .delete(name=resource_name)
    )
    response = request.execute()
    print("Deleted {} resource with ID {}.".format(resource_type, resource_id))

    return response


# [END healthcare_delete_resource]


# [START healthcare_get_resource]
def get_resource(
    project_id, cloud_region, dataset_id, fhir_store_id, resource_type, resource_id,
):
    """Reads a FHIR resource."""
    client = get_client()

    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )

    resource_name = "{}/fhirStores/{}/fhir/{}/{}".format(
        fhir_store_parent, fhir_store_id, resource_type, resource_id
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .read(name=resource_name)
    )
    response = request.execute()

    print("Got {} resource:".format(response["resourceType"]))
    print(json.dumps(response, indent=2))

    return response


# [END healthcare_get_resource]


# [START healthcare_list_resource_history]
def list_resource_history(
    project_id, cloud_region, dataset_id, fhir_store_id, resource_type, resource_id,
):
    """Gets the history of a resource."""
    client = get_client()

    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )

    resource_name = "{}/fhirStores/{}/fhir/{}/{}".format(
        fhir_store_parent, fhir_store_id, resource_type, resource_id
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .history(name=resource_name)
    )
    response = request.execute()

    print(
        "History for {} resource:".format(
            response["entry"][0]["resource"]["resourceType"]
        )
    )
    print(json.dumps(response, indent=2))

    return response


# [END healthcare_list_resource_history]


# [START healthcare_get_resource_history]
def get_resource_history(
    project_id,
    cloud_region,
    dataset_id,
    fhir_store_id,
    resource_type,
    resource_id,
    version_id,
):
    """Gets the contents of a version (current or historical) of a FHIR resource
    by version ID.
    """
    client = get_client()

    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )

    resource_name = "{}/fhirStores/{}/fhir/{}/{}/_history/{}".format(
        fhir_store_parent, fhir_store_id, resource_type, resource_id, version_id
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .vread(name=resource_name)
    )
    response = request.execute()

    print("Got history for {} resource:".format(resource_type))
    print(json.dumps(response, indent=2))

    return response


# [END healthcare_get_resource_history]


# [START healthcare_update_resource]
def update_resource(
    project_id, cloud_region, dataset_id, fhir_store_id, resource_type, resource_id,
):
    """Updates an existing resource."""
    client = get_client_fhir()

    fhir_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, cloud_region, dataset_id
    )

    resource_name = "{}/fhirStores/{}/fhir/{}/{}".format(
        fhir_store_parent, fhir_store_id, resource_type, resource_id
    )

    body = {"resourceType": resource_type, "active": True, "id": resource_id}

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .update(name=resource_name, body=body)
    )
    response = request.execute()

    print("Updated {} resource:".format(response["resourceType"]))
    print(json.dumps(response, indent=2))

    return response


# [END healthcare_update_resource]


# [START healthcare_search_resources_get]
def search_resources_get(
    project_id, cloud_region, dataset_id, fhir_store_id, resource_type,
):
    """
    Searches resources in the given FHIR store using the
    searchResources GET method.
    """
    client = get_client()

    fhir_store_name = "projects/{}/locations/{}/datasets/{}/fhirStores/{}".format(
        project_id, cloud_region, dataset_id, fhir_store_id
    )

    body = {"resourceType": resource_type}
    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .search(parent=fhir_store_name, body=body)
    )
    response = request.execute()

    print(
        "Using GET request, found a total of {} {} resources:".format(
            response["total"], resource_type
        )
    )
    print(json.dumps(response, indent=2))

    return response


# [END healthcare_search_resources_get]


# [END healthcare_fhir_execute_bundle]


def parse_command_line_args():
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--project_id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help="GCP project name",
    )

    parser.add_argument("--cloud_region", default="us-central1", help="GCP region")

    parser.add_argument("--dataset_id", default=None, help="Name of dataset")

    parser.add_argument("--fhir_store_id", default=None, help="Name of FHIR store")

    parser.add_argument(
        "--resource_type",
        default=None,
        help="The type of resource. First letter must be capitalized",
    )

    parser.add_argument(
        "--resource_id", default=None, help="Identifier for a FHIR resource"
    )

    parser.add_argument(
        "--patient_id",
        default=None,
        help="Identifier for a Patient resource. Can be used as a reference "
        "for an Encounter/Observation",
    )

    parser.add_argument(
        "--uri_prefix", default=None, help="Prefix of gs:// URIs for import and export"
    )

    parser.add_argument("--version_id", default=None, help="Version of a FHIR resource")

    command = parser.add_subparsers(dest="command")

    command.add_parser("create-patient", help=create_patient.__doc__)
    command.add_parser("create-encounter", help=create_encounter.__doc__)
    command.add_parser("delete-resource", help=delete_resource.__doc__)
    command.add_parser("get-resource", help=get_resource.__doc__)
    command.add_parser("list-resource-history", help=list_resource_history.__doc__)
    command.add_parser("get-resource-history", help=get_resource_history.__doc__)
    command.add_parser("update-resource", help=update_resource.__doc__)
    command.add_parser("search-resources-get", help=search_resources_get.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print(
            "You must specify a project ID or set the "
            '"GOOGLE_CLOUD_PROJECT" environment variable.'
        )
        return

    elif args.command == "create-patient":
        create_patient(
            args.project_id, args.cloud_region, args.dataset_id, args.fhir_store_id,
        )

    elif args.command == "create-encounter":
        create_encounter(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.patient_id,
        )

    elif args.command == "delete-resource":
        delete_resource(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "get-resource":
        get_resource(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "list-resource-history":
        list_resource_history(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "get-resource-history":
        get_resource_history(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
            args.version_id,
        )

    elif args.command == "update-resource":
        update_resource(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "search-resources-get":
        search_resources_get(
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
        )


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == "__main__":
    main()
