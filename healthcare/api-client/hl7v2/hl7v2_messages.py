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

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


# [START healthcare_get_client]
def get_client(service_account_json, api_key):
    """Returns an authorized API client by discovering the Healthcare API and
    creating a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1alpha'
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


# [START healthcare_create_hl7v2_message]
def create_hl7v2_message(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_file):
    """Creates an HL7v2 message and sends a notification to the
    Cloud Pub/Sub topic.
    """
    client = get_client(service_account_json, api_key)
    hl7v2_parent = 'projects/{}/locations/{}'.format(project_id, cloud_region)
    hl7v2_store_name = '{}/datasets/{}/hl7V2Stores/{}'.format(
        hl7v2_parent, dataset_id, hl7v2_store_id)

    with open(hl7v2_message_file) as hl7v2_message:
        hl7v2_message_content = json.load(hl7v2_message)

    request = client.projects().locations().datasets().hl7V2Stores(
    ).messages().create(parent=hl7v2_store_name, body=hl7v2_message_content)

    try:
        response = request.execute()
        print('Created HL7v2 message from file: {}'.format(hl7v2_message_file))
        return response
    except HttpError as e:
        print('Error, HL7v2 message not created: {}'.format(e))
        return ""
# [END healthcare_create_hl7v2_message]


# [START healthcare_delete_hl7v2_message]
def delete_hl7v2_message(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_id):
    """Deletes an HL7v2 message."""
    client = get_client(service_account_json, api_key)
    hl7v2_parent = 'projects/{}/locations/{}'.format(project_id, cloud_region)
    hl7v2_message = '{}/datasets/{}/hl7V2Stores/{}/messages/{}'.format(
        hl7v2_parent, dataset_id, hl7v2_store_id, hl7v2_message_id)

    request = client.projects().locations().datasets(
    ).hl7V2Stores().messages().delete(name=hl7v2_message)

    try:
        response = request.execute()
        print('Deleted HL7v2 message with ID: {}'.format(hl7v2_message_id))
        return response
    except HttpError as e:
        print('Error, HL7v2 message not deleted: {}'.format(e))
        return ""
# [END healthcare_delete_hl7v2_message]


# [START healthcare_get_hl7v2_message]
def get_hl7v2_message(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_id):
    """Gets an HL7v2 message."""
    client = get_client(service_account_json, api_key)
    hl7v2_parent = 'projects/{}/locations/{}'.format(project_id, cloud_region)
    hl7v2_message_name = '{}/datasets/{}/hl7V2Stores/{}/messages/{}'.format(
        hl7v2_parent, dataset_id, hl7v2_store_id, hl7v2_message_id)

    msgs = client.projects().locations().datasets().hl7V2Stores().messages()
    message = msgs.get(name=hl7v2_message_name).execute()

    print('Name: {}'.format(message.get('name')))
    print('Data: {}'.format(message.get('data')))
    print('Creation time: {}'.format(message.get('createTime')))
    print('Sending facility: {}'.format(message.get('sendFacility')))
    print('Time sent: {}'.format(message.get('sendTime')))
    print('Message type: {}'.format(message.get('messageType')))
    print('Patient IDs:')
    patient_ids = message.get('patientIds')
    for patient_id in patient_ids:
        print('\tPatient value: {}'.format(patient_id.get('value')))
        print('\tPatient type: {}'.format(patient_id.get('type')))
    print('Labels: {}'.format(message.get('labels')))

    print(message)
    return message
# [END healthcare_get_hl7v2_message]


# [START healthcare_ingest_hl7v2_message]
def ingest_hl7v2_message(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_file):
    """Ingests a new HL7v2 message from the hospital and sends a notification
    to the Cloud Pub/Sub topic. Return is an HL7v2 ACK message if the message
    was successfully stored.
    """
    client = get_client(service_account_json, api_key)
    hl7v2_parent = 'projects/{}/locations/{}'.format(project_id, cloud_region)
    hl7v2_store_name = '{}/datasets/{}/hl7V2Stores/{}'.format(
        hl7v2_parent, dataset_id, hl7v2_store_id)

    with open(hl7v2_message_file) as hl7v2_message:
        hl7v2_message_content = json.load(hl7v2_message)

    request = client.projects().locations().datasets().hl7V2Stores(
    ).messages().ingest(parent=hl7v2_store_name, body=hl7v2_message_content)

    try:
        response = request.execute()
        print('Ingested HL7v2 message from file: {}'.format(
            hl7v2_message_file))
        return response
    except HttpError as e:
        print('Error, HL7v2 message not ingested: {}'.format(e))
        return ""
# [END healthcare_ingest_hl7v2_message]


# [START healthcare_list_hl7v2_messages]
def list_hl7v2_messages(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id):
    """Lists all the messages in the given HL7v2 store with support for
    filtering.
    """
    client = get_client(service_account_json, api_key)
    hl7v2_messages_parent = 'projects/{}/locations/{}/datasets/{}'.format(
        project_id, cloud_region, dataset_id)
    hl7v2_message_path = '{}/hl7V2Stores/{}'.format(
        hl7v2_messages_parent, hl7v2_store_id)

    hl7v2_messages = client.projects().locations().datasets().hl7V2Stores(
    ).messages().list(parent=hl7v2_message_path).execute().get('messages', [])

    for hl7v2_message in hl7v2_messages:
        print(hl7v2_message)

    return hl7v2_messages
# [END healthcare_list_hl7v2_messages]


# [START healthcare_patch_hl7v2_message]
def patch_hl7v2_message(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_id,
        label_key,
        label_value):
    """Updates the message."""
    client = get_client(service_account_json, api_key)
    hl7v2_message_parent = 'projects/{}/locations/{}'.format(
        project_id, cloud_region, dataset_id, hl7v2_store_id)
    hl7v2_message_name = '{}/datasets/{}/hl7V2Stores/{}/messages/{}'.format(
        hl7v2_message_parent, dataset_id, hl7v2_store_id, hl7v2_message_id)

    patch = {
        'labels': {
            label_key: label_value
        }
    }

    request = client.projects().locations().datasets().hl7V2Stores().messages(
    ).patch(name=hl7v2_message_name, updateMask='labels', body=patch)

    try:
        response = request.execute()
        print(
            'Patched HL7v2 message {} with labels:\n\t{}: {}'.format(
                hl7v2_message_id,
                label_key,
                label_value))
        return response
    except HttpError as e:
        print('Error, HL7v2 message not patched: {}'.format(e))
        return ""
# [END healthcare_patch_hl7v2_message]


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
        help='GCP region')

    parser.add_argument(
        '--dataset_id',
        default=None,
        help='Name of dataset')

    parser.add_argument(
        '--hl7v2_store_id',
        default=None,
        help='Name of HL7v2 store')

    parser.add_argument(
        '--hl7v2_message_file',
        default=None,
        help='A file containing a base64-encoded HL7v2 message')

    parser.add_argument(
        '--hl7v2_message_id',
        default=None,
        help='The identifier for the message returned by the server'
    )

    parser.add_argument(
        '--label_key',
        default=None,
        help='Arbitrary label key to apply to the message'
    )

    parser.add_argument(
        '--label_value',
        default=None,
        help='Arbitrary label value to apply to the message'
    )

    command = parser.add_subparsers(dest='command')

    command.add_parser(
        'create-hl7v2-message',
        help=create_hl7v2_message.__doc__)
    command.add_parser(
        'delete-hl7v2-message',
        help=delete_hl7v2_message.__doc__)
    command.add_parser('get-hl7v2-message', help=get_hl7v2_message.__doc__)
    command.add_parser(
        'ingest-hl7v2-message',
        help=ingest_hl7v2_message.__doc__)
    command.add_parser('list-hl7v2-messages', help=list_hl7v2_messages.__doc__)
    command.add_parser(
        'patch-hl7v2-message',
        help=patch_hl7v2_message.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print('You must specify a project ID or set the '
              '"GOOGLE_CLOUD_PROJECT" environment variable.')
        return

    elif args.command == 'create-hl7v2-message':
        create_hl7v2_message(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.hl7v2_store_id,
            args.hl7v2_message_file)

    elif args.command == 'delete-hl7v2-message':
        delete_hl7v2_message(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.hl7v2_store_id,
            args.hl7v2_message_id)

    elif args.command == 'get-hl7v2-message':
        get_hl7v2_message(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.hl7v2_store_id,
            args.hl7v2_message_id)

    elif args.command == 'ingest-hl7v2-message':
        ingest_hl7v2_message(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.hl7v2_store_id,
            args.hl7v2_message_file)

    elif args.command == 'list-hl7v2-messages':
        list_hl7v2_messages(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.hl7v2_store_id)

    elif args.command == 'patch-hl7v2-message':
        patch_hl7v2_message(
            args.service_account_json,
            args.api_key,
            args.project_id,
            args.cloud_region,
            args.dataset_id,
            args.hl7v2_store_id,
            args.hl7v2_message_id,
            args.label_key,
            args.label_value)


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == '__main__':
    main()
