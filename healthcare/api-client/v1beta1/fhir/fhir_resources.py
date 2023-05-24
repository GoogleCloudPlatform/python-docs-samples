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

from google.auth.transport import requests
from google.oauth2 import service_account


_BASE_URL = "https://healthcare.googleapis.com/v1beta1"


def get_session(service_account_json):
    """
    Returns an authorized Requests Session class using the service account
    credentials JSON. This class is used to perform requests to the
    Healthcare API endpoint.
    """

    # Pass in the credentials and project ID. If none supplied, get them
    # from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        service_account_json
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    return session


def create_patient(
    service_account_json, base_url, project_id, cloud_region, dataset_id, fhir_store_id
):
    """Creates a new Patient resource in a FHIR store."""
    url = f"{base_url}/projects/{project_id}/locations/{cloud_region}"

    fhir_store_path = "{}/datasets/{}/fhirStores/{}/fhir/Patient".format(
        url, dataset_id, fhir_store_id
    )

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    body = {
        "name": [{"use": "official", "family": "Smith", "given": ["Darcy"]}],
        "gender": "female",
        "birthDate": "1970-01-01",
        "resourceType": "Patient",
    }

    response = session.post(fhir_store_path, headers=headers, json=body)
    response.raise_for_status()

    resource = response.json()

    print("Created Patient resource with ID {}".format(resource["id"]))

    return response


def create_encounter(
    service_account_json,
    base_url,
    project_id,
    cloud_region,
    dataset_id,
    fhir_store_id,
    patient_id,
):
    """Creates a new Encounter resource in a FHIR store based on a Patient."""
    url = f"{base_url}/projects/{project_id}/locations/{cloud_region}"

    fhir_store_path = "{}/datasets/{}/fhirStores/{}/fhir/Encounter".format(
        url, dataset_id, fhir_store_id
    )

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    body = {
        "status": "finished",
        "class": {
            "system": "http://hl7.org/fhir/v3/ActCode",
            "code": "IMP",
            "display": "inpatient encounter",
        },
        "reasonCode": [
            {
                "text": "The patient had an abnormal heart rate. She was concerned about this."
            }
        ],
        "subject": {"reference": f"Patient/{patient_id}"},
        "resourceType": "Encounter",
    }

    response = session.post(fhir_store_path, headers=headers, json=body)
    response.raise_for_status()

    resource = response.json()

    print("Created Encounter resource with ID {}".format(resource["id"]))

    return response


def create_observation(
    service_account_json,
    base_url,
    project_id,
    cloud_region,
    dataset_id,
    fhir_store_id,
    patient_id,
    encounter_id,
):
    """
    Creates a new Observation resource in a FHIR store based on
    an Encounter.
    """
    url = f"{base_url}/projects/{project_id}/locations/{cloud_region}"

    fhir_store_path = "{}/datasets/{}/fhirStores/{}/fhir/Observation".format(
        url, dataset_id, fhir_store_id
    )

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    body = {
        "resourceType": "Observation",
        "status": "final",
        "subject": {"reference": f"Patient/{patient_id}"},
        "effectiveDateTime": "2020-01-01T00:00:00+00:00",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "8867-4",
                    "display": "Heart rate",
                }
            ]
        },
        "valueQuantity": {"value": 55, "unit": "bpm"},
        "encounter": {"reference": f"Encounter/{encounter_id}"},
    }
    response = session.post(fhir_store_path, headers=headers, json=body)
    response.raise_for_status()

    resource = response.json()

    print("Created Observation resource with ID {}".format(resource["id"]))

    return response


def delete_resource(
    service_account_json,
    base_url,
    project_id,
    cloud_region,
    dataset_id,
    fhir_store_id,
    resource_type,
    resource_id,
):
    """
    Deletes a FHIR resource. Regardless of whether the operation succeeds or
    fails, the server returns a 200 OK HTTP status code. To check that the
    resource was successfully deleted, search for or get the resource and
    see if it exists.
    """
    url = f"{base_url}/projects/{project_id}/locations/{cloud_region}"

    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/{}/{}".format(
        url, dataset_id, fhir_store_id, resource_type, resource_id
    )

    # Make an authenticated API request
    session = get_session(service_account_json)

    response = session.delete(resource_path)
    print(f"Deleted {resource_type} resource with ID {resource_id}.")

    return response


# [START healthcare_conditional_update_resource]
def conditional_update_resource(
    service_account_json,
    base_url,
    project_id,
    cloud_region,
    dataset_id,
    fhir_store_id,
    patient_id,
    encounter_id,
):
    """
    If a resource is found based on the search criteria specified in
    the query parameters, updates the entire contents of that resource.
    """
    url = f"{base_url}/projects/{project_id}/locations/{cloud_region}"

    # The search query in this request updates all Observations
    # using the Observation's identifier (ABC-12345 in my-code-system)
    # so that their 'status' is 'cancelled'.
    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/Observation".format(
        url, dataset_id, fhir_store_id
    )

    # Make an authenticated API request
    session = get_session(service_account_json)

    body = {
        "resourceType": "Observation",
        "status": "cancelled",
        "subject": {"reference": f"Patient/{patient_id}"},
        "effectiveDateTime": "2020-01-01T00:00:00+00:00",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "8867-4",
                    "display": "Heart rate",
                }
            ]
        },
        "valueQuantity": {"value": 55, "unit": "bpm"},
        "encounter": {"reference": f"Encounter/{encounter_id}"},
    }

    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    params = {"identifier": "my-code-system|ABC-12345"}

    response = session.put(resource_path, headers=headers, params=params, json=body)

    response.raise_for_status()
    resource = response.json()

    print(
        "Conditionally updated Observations with the identifier "
        "'my-code-system|ABC-12345' to have a 'status' of "
        "'cancelled'."
    )
    print(json.dumps(resource, indent=2))

    return resource


# [END healthcare_conditional_update_resource]


# [START healthcare_conditional_delete_resource]
def conditional_delete_resource(
    service_account_json, base_url, project_id, cloud_region, dataset_id, fhir_store_id
):
    """Deletes FHIR resources that match a search query."""
    url = f"{base_url}/projects/{project_id}/locations/{cloud_region}"

    # The search query in this request deletes all Observations
    # with a status of 'cancelled'.
    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/Observation".format(
        url, dataset_id, fhir_store_id
    )
    # The search query is passed in as a query string parameter.
    params = {"status": "cancelled"}

    # Make an authenticated API request
    session = get_session(service_account_json)

    response = session.delete(resource_path, params=params)
    print(response.url)
    if response.status_code != 404:  # Don't consider missing to be error
        response.raise_for_status()

    print("Conditionally deleted all Observations with status='cancelled'.")

    return response


# [END healthcare_conditional_delete_resource]


# [START healthcare_conditional_patch_resource]
def conditional_patch_resource(
    service_account_json, base_url, project_id, cloud_region, dataset_id, fhir_store_id
):
    """
    If a resource is found based on the search criteria specified in
    the query parameters, updates part of that resource by
    applying the operations specified in a JSON Patch document.
    """
    url = f"{base_url}/projects/{project_id}/locations/{cloud_region}"

    # The search query in this request updates all Observations
    # if the subject of the Observation is a particular patient.
    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/Observation".format(
        url, dataset_id, fhir_store_id
    )

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {"Content-Type": "application/json-patch+json"}

    body = json.dumps(
        [
            {
                "op": "replace",
                "path": "/valueQuantity/value",
                # Sets the BPM for all matching Observations to 80. This
                # is the portion of the request being patched.
                "value": 80,
            }
        ]
    )

    # The search query is passed in as a query string parameter.
    params = {"identifier": "my-code-system|ABC-12345"}

    response = session.patch(resource_path, headers=headers, params=params, data=body)
    response.raise_for_status()

    print(response.url)

    resource = response.json()

    print(
        "Conditionally patched all Observations with the "
        "identifier 'my-code-system|ABC-12345' to use a BPM of 80."
    )
    print(json.dumps(resource, indent=2))

    return resource


# [END healthcare_conditional_patch_resource]


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

    parser.add_argument("--base_url", default=_BASE_URL, help="Healthcare API URL.")

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
        "--encounter_id",
        default=None,
        help="Identifier for an Encounter resource. Can be used as a "
        "reference for an Observation",
    )

    command = parser.add_subparsers(dest="command")

    command.add_parser("create-patient", help=create_patient.__doc__)
    command.add_parser("create-encounter", help=create_encounter.__doc__)
    command.add_parser("create-observation", help=create_observation.__doc__)
    command.add_parser("delete-resource", help=delete_resource.__doc__)
    command.add_parser(
        "conditional-delete-resource", help=conditional_delete_resource.__doc__
    )
    command.add_parser(
        "conditional-update-resource", help=conditional_update_resource.__doc__
    )
    command.add_parser(
        "conditional-patch-resource", help=conditional_patch_resource.__doc__
    )

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
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
        )

    elif args.command == "create-encounter":
        create_encounter(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.patient_id,
        )

    elif args.command == "create-observation":
        create_observation(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.patient_id,
            args.encounter_id,
        )

    elif args.command == "delete-resource":
        delete_resource(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id,
        )

    elif args.command == "conditional-delete-resource":
        conditional_delete_resource(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
        )

    elif args.command == "conditional-update-resource":
        conditional_update_resource(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.patient_id,
            args.encounter_id,
        )

    elif args.command == "conditional-patch-resource":
        conditional_patch_resource(
            args.service_account_json,
            args.base_url,
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
