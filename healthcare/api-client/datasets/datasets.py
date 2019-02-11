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

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


# [START healthcare_get_client]
def get_client(service_account_json, api_key):
    """Returns an authorized API client by discovering the Healthcare API and
    creating a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1alpha2'
    discovery_api = 'https://healthcare.googleapis.com/$discovery/rest'
    service_name = 'healthcare'

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?labels=CHC_ALPHA&version={}&key={}'.format(
        discovery_api, api_version, api_key)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials)
# [END healthcare_get_client]


# [START healthcare_create_dataset]
def create_dataset(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id):
    """Creates a dataset."""
    client = get_client(service_account_json, api_key)
    dataset_parent = 'projects/{}/locations/{}'.format(
        project_id, cloud_region)

    body = {}

    request = client.projects().locations().datasets().create(
        parent=dataset_parent, body=body, datasetId=dataset_id)

    try:
        response = request.execute()
        print('Created dataset: {}'.format(dataset_id))
        return response
    except HttpError as e:
        print('Error, dataset not created: {}'.format(e))
        return ""
# [END healthcare_create_dataset]


# [START healthcare_delete_dataset]
def delete_dataset(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id):
    """Deletes a dataset."""
    client = get_client(service_account_json, api_key)
    dataset_name = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)

    request = client.projects().locations().datasets().delete(
        name=dataset_name)

    try:
        response = request.execute()
        print('Deleted dataset: {}'.format(dataset_id))
        return response
    except HttpError as e:
        print('Error, dataset not deleted: {}'.format(e))
        return ""
# [END healthcare_delete_dataset]


# [START healthcare_get_dataset]
def get_dataset(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id):
    """Gets any metadata associated with a dataset."""
    client = get_client(service_account_json, api_key)
    dataset_name = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)

    datasets = client.projects().locations().datasets()
    dataset = datasets.get(name=dataset_name).execute()

    print('Name: {}'.format(dataset.get('name')))
    print('Time zone: {}'.format(dataset.get('timeZone')))

    return dataset
# [END healthcare_get_dataset]


# [START healthcare_list_datasets]
def list_datasets(service_account_json, api_key, project_id, cloud_region):
    """Lists the datasets in the project."""
    client = get_client(service_account_json, api_key)
    dataset_parent = 'projects/{}/locations/{}'.format(
        project_id, cloud_region)

    datasets = client.projects().locations().datasets().list(
        parent=dataset_parent).execute().get('datasets', [])

    for dataset in datasets:
        print('Dataset: {}\nTime zone: {}'.format(
            dataset.get('name'),
            dataset.get('timeZone')
        ))

    return datasets
# [END healthcare_list_datasets]


# [START healthcare_patch_dataset]
def patch_dataset(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        time_zone):
    """Updates dataset metadata."""
    client = get_client(service_account_json, api_key)
    dataset_parent = 'projects/{}/locations/{}'.format(
        project_id, cloud_region)
    dataset_name = '{}/datasets/{}'.format(dataset_parent, dataset_id)

    # Sets the time zone to GMT
    patch = {
        'timeZone': time_zone
    }

    request = client.projects().locations().datasets().patch(
        name=dataset_name, updateMask='timeZone', body=patch)

    try:
        response = request.execute()
        print(
            'Patched dataset {} with time zone: {}'.format(
                dataset_id,
                time_zone))
        return response
    except HttpError as e:
        print('Error, dataset not patched: {}'.format(e))
        return ""
# [END healthcare_patch_dataset]


# [START healthcare_deidentify_dataset]
def deidentify_dataset(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        destination_dataset_id,
        keeplist_tags):
    """Creates a new dataset containing de-identified data
    from the source dataset.
    """
    client = get_client(service_account_json, api_key)
    source_dataset = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)
    destination_dataset = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, destination_dataset_id)

    body = {
        'destinationDataset': destination_dataset,
        'config': {
            'dicom': {
                'keepList': {
                    'tags': [
                        'Columns',
                        'NumberOfFrames',
                        'PixelRepresentation',
                        'MediaStorageSOPClassUID',
                        'MediaStorageSOPInstanceUID',
                        'Rows',
                        'SamplesPerPixel',
                        'BitsAllocated',
                        'HighBit',
                        'PhotometricInterpretation',
                        'BitsStored',
                        'PatientID',
                        'TransferSyntaxUID',
                        'SOPInstanceUID',
                        'StudyInstanceUID',
                        'SeriesInstanceUID',
                        'PixelData'
                    ]
                }
            }
        }
    }

    request = client.projects().locations().datasets().deidentify(
        sourceDataset=source_dataset, body=body)

    try:
        response = request.execute()
        print(
            'Data in dataset {} de-identified.'
            'De-identified data written to {}'.format(
                dataset_id,
                destination_dataset_id))
        return response
    except HttpError as e:
        print('Error, data could not be deidentified: {}'.format(e))
        return ""
# [END healthcare_deidentify_dataset]


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
        '--api_key',
        default=os.environ.get("API_KEY"),
        help='Your API key.')

    parser.add_argument(
        '--project_id',
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help='GCP project name')

    parser.add_argument(
        '--cloud_region',
        default='us-central1',
        help='GCP cloud region')

    parser.add_argument(
        '--dataset_id',
        default=None,
        help='Name of dataset')

    parser.add_argument(
        '--time_zone',
        default=None,
        help='The default timezone used by a dataset')

    parser.add_argument(
        '--destination_dataset_id',
        default=None,
        help='The name of the new dataset where the de-identified data '
        'will be written')

    parser.add_argument(
        '--keeplist_tags',
        default=None,
        help='The data to keeplist, for example "PatientID" '
        'or "StudyInstanceUID"')

    command = parser.add_subparsers(dest='command')

    command.add_parser('create-dataset', help=create_dataset.__doc__)
    command.add_parser('delete-dataset', help=delete_dataset.__doc__)
    command.add_parser('get-dataset', help=get_dataset.__doc__)
    command.add_parser('list-datasets', help=list_datasets.__doc__)
    command.add_parser('patch-dataset', help=patch_dataset.__doc__)

    command.add_parser('deidentify-dataset', help=deidentify_dataset.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print('You must specify a project ID or set the'
              '"GOOGLE_CLOUD_PROJECT" environment variable.')
        return

    elif args.command == 'create-dataset':
        create_dataset(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id)

    elif args.command == 'delete-dataset':
        delete_dataset(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id)

    elif args.command == 'get-dataset':
        get_dataset(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id)

    elif args.command == 'list-datasets':
        list_datasets(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region)

    elif args.command == 'patch-dataset':
        patch_dataset(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.time_zone)

    elif args.command == 'deidentify-dataset':
        deidentify_dataset(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.destination_dataset_id,
            args.keeplist_tags)


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == '__main__':
    main()
