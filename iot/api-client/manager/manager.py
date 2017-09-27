#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
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


"""
Example of using the Google Cloud IoT Core device manager to administer
devices.

Usage example:

    python manager.py \\
      --project_id=my-project-id \\
      --pubsub_topic=projects/my-project-id/topics/my-topic-id \\
      --ec_public_key_file=../ec_public.pem \\
      --rsa_certificate_file=../rsa_cert.pem \\
      --service_account_json=$HOME/service_account.json
      list
"""

import argparse
import io
import os
import sys
import time

from google.cloud import pubsub
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def create_iot_topic(topic_name):
    """Creates a PubSub Topic and grants access to Cloud IoT Core."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    topic.create()

    topic = pubsub_client.topic(topic_name)
    policy = topic.get_iam_policy()
    publishers = policy.get('roles/pubsub.publisher', [])
    if hasattr(publishers, "append"):
        publishers.append(policy.service_account(
                'cloud-iot@system.gserviceaccount.com'))
    else:
        publishers.add(policy.service_account(
                'cloud-iot@system.gserviceaccount.com'))
    policy['roles/pubsub.publisher'] = publishers
    topic.set_iam_policy(policy)

    return topic


def get_client(service_account_json):
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
            service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
            discovery_api, api_version)

    return discovery.build(
            service_name,
            api_version,
            discoveryServiceUrl=discovery_url,
            credentials=scoped_credentials)


def create_rs256_device(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        certificate_file):
    """Create a new device with the given id, using RS256 for
    authentication."""
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    client = get_client(service_account_json)
    with io.open(certificate_file) as f:
        certificate = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        'id': device_id,
        'credentials': [{
            'publicKey': {
                'format': 'RSA_X509_PEM',
                'key': certificate
            }
        }]
    }

    devices = client.projects().locations().registries().devices()
    return devices.create(parent=registry_name, body=device_template).execute()


def create_es256_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id, public_key_file):
    """Create a new device with the given id, using ES256 for
    authentication."""
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    client = get_client(service_account_json)
    with io.open(public_key_file) as f:
        public_key = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        'id': device_id,
        'credentials': [{
            'publicKey': {
                'format': 'ES256_PEM',
                'key': public_key
            }
        }]
    }

    devices = client.projects().locations().registries().devices()
    return devices.create(parent=registry_name, body=device_template).execute()


def create_unauth_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Create a new device without authentication."""
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    client = get_client(service_account_json)
    device_template = {
        'id': device_id,
    }

    devices = client.projects().locations().registries().devices()
    return devices.create(parent=registry_name, body=device_template).execute()


def delete_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Delete the device with the given id."""
    print('Delete device')
    client = get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    device_name = '{}/devices/{}'.format(registry_name, device_id)

    devices = client.projects().locations().registries().devices()
    return devices.delete(name=device_name).execute()


def delete_registry(
       service_account_json, project_id, cloud_region, registry_id):
    """Deletes the specified registry."""
    print('Delete registry')
    client = get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    registries = client.projects().locations().registries()
    return registries.delete(name=registry_name).execute()


def get_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Retrieve the device with the given id."""
    print('Getting device')
    client = get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    device_name = '{}/devices/{}'.format(registry_name, device_id)
    devices = client.projects().locations().registries().devices()
    device = devices.get(name=device_name).execute()

    print('Id : {}'.format(device.get('id')))
    print('Name : {}'.format(device.get('name')))
    print('Credentials:')
    if device.get('credentials') is not None:
        for credential in device.get('credentials'):
            keyinfo = credential.get('publicKey')
            print('\tcertificate: \n{}'.format(keyinfo.get('key')))
            print('\tformat : {}'.format(keyinfo.get('format')))
            print('\texpiration: {}'.format(credential.get('expirationTime')))

    print('Config:')
    print('\tdata: {}'.format(device.get('config').get('data')))
    print('\tversion: {}'.format(device.get('config').get('version')))
    print('\tcloudUpdateTime: {}'.format(device.get('config').get(
            'cloudUpdateTime')))

    return device


def get_state(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Retrieve a device's state blobs."""
    client = get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    device_name = '{}/devices/{}'.format(registry_name, device_id)
    devices = client.projects().locations().registries().devices()
    state = devices.states().list(name=device_name, numStates=5).execute()

    print('State: {}\n'.format(state))

    return state


def list_devices(
        service_account_json, project_id, cloud_region, registry_id):
    """List all devices in the registry."""
    print('Listing devices')
    registry_path = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)
    client = get_client(service_account_json)
    devices = client.projects().locations().registries().devices(
            ).list(parent=registry_path).execute().get('devices', [])

    for device in devices:
            print('Device: {} : {}'.format(
                    device.get('numId'),
                    device.get('id')))

    return devices


def list_registries(service_account_json, project_id, cloud_region):
    """List all registries in the project."""
    print('Listing Registries')
    registry_path = 'projects/{}/locations/{}'.format(
            project_id, cloud_region)
    client = get_client(service_account_json)
    registries = client.projects().locations().registries().list(
        parent=registry_path).execute().get('deviceRegistries', [])

    for registry in registries:
            print('id: {}\n\tname: {}'.format(
                    registry.get('id'),
                    registry.get('name')))

    return registries


def create_registry(
        service_account_json, project_id, cloud_region, pubsub_topic,
        registry_id):
    """ Creates a registry and returns the result. Returns an empty result if
    the registry already exists."""
    client = get_client(service_account_json)
    registry_parent = 'projects/{}/locations/{}'.format(
            project_id,
            cloud_region)
    body = {
        'eventNotificationConfigs': [{
            'pubsubTopicName': pubsub_topic
        }],
        'id': registry_id
    }
    request = client.projects().locations().registries().create(
        parent=registry_parent, body=body)

    try:
        response = request.execute()
        print('Created registry')
        return response
    except HttpError:
        print('Error, registry not created')
        return ""


def get_registry(
        service_account_json, project_id, cloud_region, registry_id):
    """ Retrieves a device registry."""
    client = get_client(service_account_json)
    registry_parent = 'projects/{}/locations/{}'.format(
            project_id,
            cloud_region)
    topic_name = '{}/registries/{}'.format(registry_parent, registry_id)
    request = client.projects().locations().registries().get(name=topic_name)
    return request.execute()


def open_registry(
        service_account_json, project_id, cloud_region, pubsub_topic,
        registry_id):
    """Gets or creates a device registry."""
    print('Creating registry')

    response = create_registry(
        service_account_json, project_id, cloud_region,
        pubsub_topic, registry_id)

    if (response is ""):
        # Device registry already exists
        print(
            'Registry {} already exists - looking it up instead.'.format(
                registry_id))
        response = get_registry(
            service_account_json, project_id, cloud_region,
            registry_id)

    print('Registry {} opened: '.format(response.get('name')))
    print(response)


def patch_es256_auth(
        service_account_json, project_id, cloud_region, registry_id,
        device_id, public_key_file):
    """Patch the device to add an ES256 public key to the device."""
    print('Patch device with ES256 certificate')
    client = get_client(service_account_json)
    registry_path = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    with io.open(public_key_file) as f:
        public_key = f.read()

    patch = {
        'credentials': [{
            'publicKey': {
                'format': 'ES256_PEM',
                'key': public_key
            }
        }]
    }

    device_name = '{}/devices/{}'.format(registry_path, device_id)

    return client.projects().locations().registries().devices().patch(
            name=device_name, updateMask='credentials', body=patch).execute()


def patch_rsa256_auth(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        public_key_file):
    """Patch the device to add an RSA256 public key to the device."""
    print('Patch device with RSA256 certificate')
    client = get_client(service_account_json)
    registry_path = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    with io.open(public_key_file) as f:
        public_key = f.read()

    patch = {
        'credentials': [{
            'publicKey': {
                'format': 'RSA_X509_PEM',
                'key': public_key
            }
        }]
    }

    device_name = '{}/devices/{}'.format(registry_path, device_id)

    return client.projects().locations().registries().devices().patch(
            name=device_name, updateMask='credentials', body=patch).execute()


def parse_command_line_args():
    """Parse command line arguments."""
    default_registry = 'cloudiot_device_manager_example_registry_{}'.format(
            int(time.time()))

    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    # Required arguments
    parser.add_argument(
            '--pubsub_topic',
            required=True,
            help=('Google Cloud Pub/Sub topic. '
                  'Format is projects/project_id/topics/topic-id'))

    # Optional arguments
    parser.add_argument(
            '--project_id',
            default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            help='GCP cloud project name.')
    parser.add_argument(
            '--ec_public_key_file',
            default=None,
            help='Path to public ES256 key file.')
    parser.add_argument(
            '--rsa_certificate_file',
            default=None,
            help='Path to RS256 certificate file.')
    parser.add_argument(
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--service_account_json',
            default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            help='Path to service account json file.')
    parser.add_argument(
            '--registry_id',
            default=default_registry,
            help='Registry id. If not set, a name will be generated.')
    parser.add_argument(
            '--device_id',
            default=None,
            help='Device id.')

    # Command subparser
    command = parser.add_subparsers(dest='command')

    command.add_parser('create-es256', help=create_es256_device.__doc__)
    command.add_parser('create-registry', help=open_registry.__doc__)
    command.add_parser('create-rsa256', help=create_rs256_device.__doc__)
    command.add_parser('create-topic', help=create_iot_topic.__doc__)
    command.add_parser('create-unauth', help=create_unauth_device.__doc__)
    command.add_parser('delete-device', help=delete_device.__doc__)
    command.add_parser('delete-registry', help=delete_registry.__doc__)
    command.add_parser('get', help=get_device.__doc__)
    command.add_parser('get-registry', help=get_registry.__doc__)
    command.add_parser('get-state', help=get_state.__doc__)
    command.add_parser('list', help=list_devices.__doc__)
    command.add_parser('list-registries', help=list_registries.__doc__)
    command.add_parser('patch-es256', help=patch_es256_auth.__doc__)
    command.add_parser('patch-rs256', help=patch_rsa256_auth.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print('You must specify a project ID or set the environment variable.')
        return

    if args.command == 'create-rsa256':
        create_rs256_device(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.rsa_certificate_file)

    elif args.command == 'create-es256':
        create_es256_device(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.ec_public_key_file)

    elif args.command == 'create-unauth':
        create_unauth_device(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id)

    elif args.command == 'create-registry':
        open_registry(
                args.service_account_json, args.project_id,
                args.cloud_region, args.pubsub_topic, args.registry_id)

    elif args.command == 'create-topic':
        create_iot_topic(args.pubsub_topic)

    elif args.command == 'delete-device':
        delete_device(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id)

    elif args.command == 'delete-registry':
        delete_registry(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id)

    elif args.command == 'get':
        get_device(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id)

    elif args.command == 'get-state':
        get_state(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id)

    elif args.command == 'list':
        list_devices(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id)

    elif args.command == 'get-registry':
        print(get_registry(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id))

    elif args.command == 'list-registries':
        list_registries(
                args.service_account_json, args.project_id,
                args.cloud_region)

    elif args.command == 'patch-es256':
        if (args.ec_public_key_file is None):
            sys.exit('Error: specify --ec_public_key_file')
        patch_es256_auth(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.ec_public_key_file)

    elif args.command == 'patch-rs256':
        if (args.rsa_certificate_file is None):
            sys.exit('Error: specify --rsa_certificate_file')
        patch_rsa256_auth(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.rsa_certificate_file)


def main():
    args = parse_command_line_args()
    run_command(args)


if __name__ == '__main__':
    main()
