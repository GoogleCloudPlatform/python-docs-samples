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
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

_BASE_URL = 'https://healthcare.googleapis.com/v1alpha'


# [START healthcare_get_session]
def get_session(service_account_json):
    """Returns an authorized Requests Session class using the service account
    credentials JSON. This class is used to perform requests to the
    Healthcare API endpoint."""

    # Pass in the credentials and project ID. If none supplied, get them
    # from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/cloud-platform'])

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    return session
# [END healthcare_get_session]


# [START healthcare_create_resource]
def create_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type):
    """Creates a new resource in a FHIR store."""
    url = '{}/projects/{}/locations/{}'.format(base_url, project_id,
                                               cloud_region)

    fhir_store_path = '{}/datasets/{}/fhirStores/{}/resources/{}'.format(
        url, dataset_id, fhir_store_id, resource_type)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }

    payload = {
        'language': 'en',
        'resourceType': resource_type
    }

    try:
        response = session.post(fhir_store_path, headers=headers, json=payload)
        response.raise_for_status()

        resource = response.json()

        print(
            'Created Resource: {} with ID {}'.format(
                resource_type,
                resource['id']))

        return response
    except HttpError as err:
        print(err)
        return ""
# [END healthcare_create_resource]


# [START healthcare_delete_resource]
def delete_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id):
    """Deletes a FHIR resource or returns NOT_FOUND if it doesn't exist."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    resource_path = '{}/datasets/{}/fhirStores/{}/resources/{}/{}'.format(
        url, dataset_id, fhir_store_id, resource_type, resource_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }

    try:
        response = session.delete(resource_path, headers=headers)
        response.raise_for_status()
        print(response)
        print('Deleted Resource: {}'.format(resource_id))
        return response
    except HttpError:
        print('Error, Resource not deleted')
        return ""
# [END healthcare_delete_resource]


# [START healthcare_get_resource]
def get_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id):
    """Gets a FHIR resource."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    resource_path = '{}/datasets/{}/fhirStores/{}/resources/{}/{}'.format(
        url, dataset_id, fhir_store_id, resource_type, resource_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }

    response = session.get(resource_path, headers=headers)
    response.raise_for_status()

    resource = response.json()

    print(json.dumps(resource, indent=2))

    return resource
# [END healthcare_get_resource]


# [START healthcare_update_resource]
def update_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id):
    """Updates an existing resource."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    resource_path = '{}/datasets/{}/fhirStores/{}/resources/{}/{}'.format(
        url, dataset_id, fhir_store_id, resource_type, resource_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }

    body = {
        'resourceType': resource_type,
        'active': True,
        'id': resource_id,
    }

    response = session.put(resource_path, headers=headers, json=body)
    response.raise_for_status()

    resource = response.json()

    print(json.dumps(resource, indent=2))

    return resource
# [END healthcare_update_resource]


# [START healthcare_patch_resource]
def patch_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        resource_id):
    """Updates part of an existing resource.."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    resource_path = '{}/datasets/{}/fhirStores/{}/resources/{}/{}'.format(
        url, dataset_id, fhir_store_id, resource_type, resource_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/json-patch+json'
    }

    body = json.dumps([
        {
            'op': 'replace',
            'path': '/active',
            'value': False
        }
    ])

    response = session.patch(resource_path, headers=headers, data=body)
    response.raise_for_status()

    resource = response.json()

    print(json.dumps(resource, indent=2))

    return resource
# [END healthcare_patch_resource]


# [START healthcare_search_resources_get]
def search_resources_get(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type):
    """Searches resources in the given FHIR store using the
    searchResources GET method."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    resource_path = '{}/datasets/{}/fhirStores/{}/resources/{}'.format(
        url, dataset_id, fhir_store_id, resource_type)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }

    response = session.get(resource_path, headers=headers)
    response.raise_for_status()

    resources = response.json()

    print(json.dumps(resources, indent=2))

    return resources
# [END healthcare_search_resources_get]


# [START healthcare_search_resources_post]
def search_resources_post(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type):
    """Searches resources in the given FHIR store using the
    _search POST method."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    resource_path = '{}/datasets/{}/fhirStores/{}/resources/{}/_search'.format(
        url, dataset_id, fhir_store_id, resource_type)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }

    response = session.post(resource_path, headers=headers)
    response.raise_for_status()

    resources = response.json()

    print(json.dumps(resources, indent=2))

    return resources
# [END healthcare_search_resources_post]


# [START healthcare_get_patient_everything]
def get_patient_everything(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_id):
    """Gets all the resources in the patient compartment."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    resource_parent = '{}/datasets/{}/fhirStores/{}'.format(
        url, dataset_id, fhir_store_id)
    resource_path = '{}/resources/Patient/{}/$everything'.format(
        resource_parent, resource_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    headers = {
        'Content-Type': 'application/fhir+json;charset=utf-8'
    }

    response = session.get(resource_path, headers=headers)
    response.raise_for_status()

    resource = response.json()

    print(json.dumps(resource, indent=2))

    return resource
# [END healthcare_get_patient_everything]


# [START healthcare_get_metadata]
def get_metadata(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id):
    """Gets the capabilities statement for a FHIR store."""
    url = '{}/projects/{}/locations/{}'.format(base_url,
                                               project_id, cloud_region)

    fhir_store_path = '{}/datasets/{}/fhirStores/{}/metadata'.format(
        url, dataset_id, fhir_store_id)

    # Make an authenticated API request
    session = get_session(service_account_json)

    response = session.get(fhir_store_path)
    response.raise_for_status()

    metadata = response.json()

    print(json.dumps(metadata, indent=2))

    return metadata
# [END healthcare_get_metadata]


def parse_command_line_args():
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--service_account_json',
        default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        help='Path to service account JSON file.')

    parser.add_argument(
        '--base_url',
        default=_BASE_URL,
        help='Healthcare API URL.')

    parser.add_argument(
        '--project_id',
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help='GCP project name')

    parser.add_argument(
        '--cloud_region',
        default='us-central1',
        help='GCP region')

    parser.add_argument(
        '--dataset_id',
        default=None,
        help='Name of dataset')

    parser.add_argument(
        '--fhir_store_id',
        default=None,
        help='Name of FHIR store')

    parser.add_argument(
        '--resource_type',
        default=None,
        help='The type of resource. First letter must be capitalized')

    parser.add_argument(
        '--resource_id',
        default=None,
        help='Name of a FHIR resource')

    command = parser.add_subparsers(dest='command')

    command.add_parser('create-resource', help=create_resource.__doc__)
    command.add_parser('delete-resource', help=create_resource.__doc__)
    command.add_parser('get-resource', help=get_resource.__doc__)
    command.add_parser('update-resource', help=update_resource.__doc__)
    command.add_parser('patch-resource', help=patch_resource.__doc__)
    command.add_parser(
        'search-resources-get',
        help=search_resources_get.__doc__)
    command.add_parser(
        'search-resources-post',
        help=search_resources_get.__doc__)
    command.add_parser(
        'get-patient-everything',
        help=get_patient_everything.__doc__)
    command.add_parser('get-metadata', help=get_metadata.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print('You must specify a project ID or set the '
              '"GOOGLE_CLOUD_PROJECT" environment variable.')
        return

    elif args.command == 'create-resource':
        create_resource(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type)

    elif args.command == 'delete-resource':
        delete_resource(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id)

    elif args.command == 'get-resource':
        get_resource(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id)

    elif args.command == 'update-resource':
        update_resource(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id)

    elif args.command == 'patch-resource':
        patch_resource(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type,
            args.resource_id)

    elif args.command == 'search-resources-get':
        search_resources_get(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type)

    elif args.command == 'search-resources-post':
        search_resources_post(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_type)

    elif args.command == 'get-patient-everything':
        get_patient_everything(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id,
            args.resource_id)

    elif args.command == 'get-metadata':
        get_metadata(
            args.service_account_json,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.fhir_store_id)


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == '__main__':
    main()
