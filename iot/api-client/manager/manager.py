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
      --cloud_region=us-central1 \\
      --service_account_json=$HOME/service_account.json \\
      list-registries
"""

import argparse
import base64
import io
import os
import sys
import time

from google.cloud import pubsub
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def create_iot_topic(project, topic_name):
    """Creates a PubSub Topic and grants access to Cloud IoT Core."""
    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project, topic_name)

    topic = pubsub_client.create_topic(topic_path)
    policy = pubsub_client.get_iam_policy(topic_path)

    policy.bindings.add(
        role='roles/pubsub.publisher',
        members=['serviceAccount:cloud-iot@system.gserviceaccount.com'])

    pubsub_client.set_iam_policy(topic_path, policy)

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
    # [START iot_create_rsa_device]
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
    # [END iot_create_rsa_device]


def create_es256_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id, public_key_file):
    """Create a new device with the given id, using ES256 for
    authentication."""
    # [START iot_create_es_device]
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
    # [END iot_create_es_device]


def create_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Create a device to bind to a gateway if it does not exist."""
    # [START create_device]
    # Check that the device doesn't already exist
    exists = False

    client = get_client(service_account_json)
    registry_path = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    devices = client.projects().locations().registries().devices(
            ).list(
                    parent=registry_path, fieldMask='config,gatewayConfig'
            ).execute().get('devices', [])

    for device in devices:
            if device.get('id') == device_id:
                exists = True

    # Create the device
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    device_template = {
        'id': device_id,
        'gatewayConfig': {
          'gatewayType': 'NON_GATEWAY',
          'gatewayAuthMethod': 'ASSOCIATION_ONLY'
        }
    }
    devices = client.projects().locations().registries().devices()

    if not exists:
        res = devices.create(
                parent=registry_name, body=device_template).execute()
        print('Created Device {}'.format(res))
    else:
        print('Device exists, skipping')
    # [END create_device]


def create_unauth_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Create a new device without authentication."""
    # [START iot_create_unauth_device]
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    client = get_client(service_account_json)
    device_template = {
        'id': device_id,
    }

    devices = client.projects().locations().registries().devices()
    return devices.create(parent=registry_name, body=device_template).execute()
    # [END iot_create_unauth_device]


def delete_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Delete the device with the given id."""
    # [START iot_delete_device]
    print('Delete device')
    client = get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    device_name = '{}/devices/{}'.format(registry_name, device_id)

    devices = client.projects().locations().registries().devices()
    return devices.delete(name=device_name).execute()
    # [END iot_delete_device]


def delete_registry(
       service_account_json, project_id, cloud_region, registry_id):
    """Deletes the specified registry."""
    # [START iot_delete_registry]
    print('Delete registry')
    client = get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    registries = client.projects().locations().registries()
    return registries.delete(name=registry_name).execute()
    # [END iot_delete_registry]


def get_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Retrieve the device with the given id."""
    # [START iot_get_device]
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
    # [END iot_get_device]


def get_state(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Retrieve a device's state blobs."""
    # [START iot_get_device_state]
    client = get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    device_name = '{}/devices/{}'.format(registry_name, device_id)
    devices = client.projects().locations().registries().devices()
    state = devices.states().list(name=device_name, numStates=5).execute()

    print('State: {}\n'.format(state))

    return state
    # [END iot_get_device_state]


def list_devices(
        service_account_json, project_id, cloud_region, registry_id):
    """List all devices in the registry."""
    # [START iot_list_devices]
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
    # [END iot_list_devices]


def list_registries(service_account_json, project_id, cloud_region):
    """List all registries in the project."""
    # [START iot_list_registries]
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
    # [END iot_list_registries]


def create_registry(
        service_account_json, project_id, cloud_region, pubsub_topic,
        registry_id):
    """ Creates a registry and returns the result. Returns an empty result if
    the registry already exists."""
    # [START iot_create_registry]
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
    # [END iot_create_registry]


def get_registry(
        service_account_json, project_id, cloud_region, registry_id):
    """ Retrieves a device registry."""
    # [START iot_get_registry]
    client = get_client(service_account_json)
    registry_parent = 'projects/{}/locations/{}'.format(
            project_id,
            cloud_region)
    topic_name = '{}/registries/{}'.format(registry_parent, registry_id)
    request = client.projects().locations().registries().get(name=topic_name)
    return request.execute()
    # [END iot_get_registry]


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
    # [START iot_patch_es]
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
    # [END iot_patch_es]


def patch_rsa256_auth(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        public_key_file):
    """Patch the device to add an RSA256 public key to the device."""
    # [START iot_patch_rsa]
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
    # [END iot_patch_rsa]


def set_config(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        version, config):
    # [START iot_set_device_config]
    print('Set device configuration')
    client = get_client(service_account_json)
    device_path = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id, cloud_region, registry_id, device_id)

    config_body = {
        'versionToUpdate': version,
        'binaryData': base64.urlsafe_b64encode(
                config.encode('utf-8')).decode('ascii')
    }

    return client.projects(
        ).locations().registries(
        ).devices().modifyCloudToDeviceConfig(
        name=device_path, body=config_body).execute()
    # [END iot_set_device_config]


def get_config_versions(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Lists versions of a device config in descending order (newest first)."""
    # [START iot_get_device_configs]
    client = get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
        project_id, cloud_region, registry_id)

    device_name = '{}/devices/{}'.format(registry_name, device_id)
    devices = client.projects().locations().registries().devices()
    configs = devices.configVersions().list(
        name=device_name).execute().get(
        'deviceConfigs', [])

    for config in configs:
        print('version: {}\n\tcloudUpdateTime: {}\n\t binaryData: {}'.format(
            config.get('version'),
            config.get('cloudUpdateTime'),
            config.get('binaryData')))

    return configs
    # [END iot_get_device_configs]


def get_iam_permissions(
        service_account_json, project_id, cloud_region, registry_id):
    """Retrieves IAM permissions for the given registry."""
    # [START iot_get_iam_policy]
    client = get_client(service_account_json)
    registry_path = 'projects/{}/locations/{}/registries/{}'.format(
        project_id, cloud_region, registry_id)

    policy = client.projects().locations().registries().getIamPolicy(
            resource=registry_path, body={}).execute()

    return policy
    # [END iot_get_iam_policy]


def set_iam_permissions(
        service_account_json, project_id, cloud_region, registry_id, role,
        member):
    """Sets IAM permissions for the given registry to a single role/member."""
    # [START iot_set_iam_policy]
    client = get_client(service_account_json)

    registry_path = 'projects/{}/locations/{}/registries/{}'.format(
        project_id, cloud_region, registry_id)
    body = {
        "policy":
        {
            "bindings":
            [{
                "members": [member],
                "role": role
            }]
        }
    }

    return client.projects().locations().registries().setIamPolicy(
            resource=registry_path, body=body).execute()
    # [END iot_set_iam_policy]


def send_command(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        command):
    """Send a command to a device."""
    # [START iot_send_command]
    print('Sending command to device')
    client = get_client(service_account_json)
    device_path = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id, cloud_region, registry_id, device_id)

    config_body = {
        'binaryData': base64.urlsafe_b64encode(
                command.encode('utf-8')).decode('ascii')
    }

    return client.projects(
        ).locations().registries(
        ).devices().sendCommandToDevice(
        name=device_path, body=config_body).execute()
    # [END iot_send_command]


def create_gateway(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        gateway_id, certificate_file, algorithm):
    """Create a gateway to bind devices to."""
    # [START create_gateway]
    # Check that the gateway doesn't already exist
    exists = False
    client = get_client(service_account_json)
    registry_path = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    devices = client.projects().locations().registries().devices(
            ).list(
                    parent=registry_path, fieldMask='config,gatewayConfig'
            ).execute().get('devices', [])

    for device in devices:
            if device.get('id') == gateway_id:
                exists = True
            print('Device: {} : {} : {} : {}'.format(
                device.get('id'),
                device.get('numId'),
                device.get('config'),
                device.get('gatewayConfig')
                ))

    # Create the gateway
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    with io.open(certificate_file) as f:
        certificate = f.read()

    if algorithm == 'ES256':
        certificate_format = 'ES256_PEM'
    else:
        certificate_format = 'RSA_X509_PEM'

    # TODO: Auth type
    device_template = {
        'id': gateway_id,
        'credentials': [{
            'publicKey': {
                'format': certificate_format,
                'key': certificate
            }
        }],
        'gatewayConfig': {
          'gatewayType': 'GATEWAY',
          'gatewayAuthMethod': 'ASSOCIATION_ONLY'
        }
    }
    devices = client.projects().locations().registries().devices()

    if not exists:
        res = devices.create(
                parent=registry_name, body=device_template).execute()
        print('Created gateway {}'.format(res))
    else:
        print('Gateway exists, skipping')
    # [END create_gateway]


def bind_device_to_gateway(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        gateway_id):
    """Binds a device to a gateway."""
    # [START bind_device_to_gateway]
    client = get_client(service_account_json)

    create_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)

    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)
    bind_request = {
        'deviceId': device_id,
        'gatewayId': gateway_id
    }
    client.projects().locations().registries().bindDeviceToGateway(
            parent=registry_name, body=bind_request).execute()
    print('Device Bound!')
    # [END bind_device_to_gateway]


def unbind_device_from_gateway(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        gateway_id):
    """Unbinds a device to a gateway."""
    # [START unbind_device_from_gateway]
    client = get_client(service_account_json)

    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)
    bind_request = {
        'deviceId': device_id,
        'gatewayId': gateway_id
    }

    res = client.projects().locations().registries().unbindDeviceFromGateway(
        parent=registry_name, body=bind_request).execute()
    print('Device unbound: {}'.format(res))
    # [END unbind_device_from_gateway]


def list_gateways(
        service_account_json, project_id, cloud_region, registry_id):
    """Lists gateways in a registry"""
    # [START list_gateways]
    client = get_client(service_account_json)
    registry_path = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    devices = client.projects().locations().registries().devices(
            ).list(
                    parent=registry_path, fieldMask='config,gatewayConfig'
            ).execute().get('devices', [])

    for device in devices:
        if device.get('gatewayConfig') is not None:
            if device.get('gatewayConfig').get('gatewayType') == 'GATEWAY':
                print('Gateway ID: {}\n\t{}'.format(device.get('id'), device))
    # [END list_gateways]


def list_devices_for_gateway(
        service_account_json, project_id, cloud_region, registry_id,
        gateway_id):
    """List devices bound to a gateway"""
    # [START list_devices_for_gateway]
    client = get_client(service_account_json)

    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    devices = client.projects().locations().registries().devices(
        ).list(
                parent=registry_name,
                gatewayListOptions_associationsGatewayId=gateway_id
        ).execute()

    found = False
    for device in devices.get('devices', []):
        found = True
        print('Device: {} : {}'.format(
                device.get('numId'),
                device.get('id')))

    if devices.get('deviceNumIds') is not None:
        for device_id in devices.get('deviceNumIds'):
            device_name = '{}/devices/{}'.format(
                    registry_name, device_id)
            device = client.projects().locations().registries().devices().get(
                    name=device_name).execute()
            print('Id: {}\n\tName: {}\n\traw: {}'.format(
                    device_id, device.get('id'), device))
    else:
        if not found:
            print('No devices bound to gateway {}'.format(gateway_id))
    # [END list_devices_for_gateway]


def parse_command_line_args():
    """Parse command line arguments."""
    default_registry = 'cloudiot_device_manager_example_registry_{}'.format(
            int(time.time()))

    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    # Optional arguments
    parser.add_argument(
            '--algorithm',
            choices=('RS256', 'ES256'),
            help='Which encryption algorithm to use to generate the JWT.')
    parser.add_argument(
            '--certificate_path',
            help='Path to public certificate.')
    parser.add_argument(
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--pubsub_topic',
            help=('Google Cloud Pub/Sub topic. '
                  'Format is projects/project_id/topics/topic-id'))
    parser.add_argument(
            '--config',
            default=None,
            help='Configuration sent to a device.')
    parser.add_argument(
            '--device_id',
            default=None,
            help='Device id.')
    parser.add_argument(
            '--ec_public_key_file',
            default=None,
            help='Path to public ES256 key file.')
    parser.add_argument(
            '--gateway_id',
            required=True,
            help='Gateway identifier.')
    parser.add_argument(
            '--member',
            default=None,
            help='Member used for IAM commands.')
    parser.add_argument(
            '--role',
            default=None,
            help='Role used for IAM commands.')
    parser.add_argument(
            '--send_command',
            default='1',
            help='The command sent to the device')
    parser.add_argument(
            '--project_id',
            default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            help='GCP cloud project name.')
    parser.add_argument(
            '--registry_id',
            default=default_registry,
            help='Registry id. If not set, a name will be generated.')
    parser.add_argument(
            '--rsa_certificate_file',
            default=None,
            help='Path to RS256 certificate file.')
    parser.add_argument(
            '--service_account_json',
            default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            help='Path to service account json file.')
    parser.add_argument(
            '--version',
            default=None,
            help='Version number for setting device configuration.')

    # Command subparser
    command = parser.add_subparsers(dest='command')

    command.add_parser(
        'bind-device-to-gateway', help=bind_device_to_gateway.__doc__)
    command.add_parser('create-es256', help=create_es256_device.__doc__)
    command.add_parser('create-gateway', help=create_gateway.__doc__)
    command.add_parser('create-registry', help=open_registry.__doc__)
    command.add_parser('create-rsa256', help=create_rs256_device.__doc__)
    command.add_parser('create-topic', help=create_iot_topic.__doc__)
    command.add_parser('create-unauth', help=create_unauth_device.__doc__)
    command.add_parser('delete-device', help=delete_device.__doc__)
    command.add_parser('delete-registry', help=delete_registry.__doc__)
    command.add_parser('get', help=get_device.__doc__)
    command.add_parser('get-config-versions', help=get_config_versions.__doc__)
    command.add_parser('get-iam-permissions', help=get_iam_permissions.__doc__)
    command.add_parser('get-registry', help=get_registry.__doc__)
    command.add_parser('get-state', help=get_state.__doc__)
    command.add_parser('list', help=list_devices.__doc__)
    command.add_parser(
        'list-devices-for-gateway', help=list_devices_for_gateway.__doc__)
    command.add_parser('list-gateways', help=list_gateways.__doc__)
    command.add_parser('list-registries', help=list_registries.__doc__)
    command.add_parser('patch-es256', help=patch_es256_auth.__doc__)
    command.add_parser('patch-rs256', help=patch_rsa256_auth.__doc__)
    command.add_parser('send-command', help=send_command.__doc__)
    command.add_parser('set-config', help=patch_rsa256_auth.__doc__)
    command.add_parser('set-iam-permissions', help=set_iam_permissions.__doc__)
    command.add_parser(
        'unbind-device-from-gateway', help=unbind_device_from_gateway.__doc__)

    return parser.parse_args()


def run_create(args):
    """Handles commands that create devices, registries, or topics."""
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

    elif args.command == 'create-gateway':
        create_gateway(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.gateway_id, args.certificate_path, args.algorithm)

    elif args.command == 'create-unauth':
        create_unauth_device(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id)

    elif args.command == 'create-registry':
        if (args.pubsub_topic is None):
            sys.exit('Error: specify --pubsub_topic')
        open_registry(
                args.service_account_json, args.project_id,
                args.cloud_region, args.pubsub_topic, args.registry_id)

    elif args.command == 'create-topic':
        if (args.pubsub_topic is None):
            sys.exit('Error: specify --pubsub_topic')
        create_iot_topic(args.project_id, args.pubsub_topic)


def run_get(args):
    if args.command == 'get':
        get_device(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id)

    elif args.command == 'get-config-versions':
        get_device(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id)

    elif args.command == 'get-state':
        get_state(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id)

    elif args.command == 'get-iam-permissions':
        print(get_iam_permissions(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id))

    elif args.command == 'get-registry':
        print(get_registry(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id))


def run_list(args):
    if args.command == 'list':
        list_devices(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id)
    elif args.command == 'list-devices-for-gateway':
        list_devices_for_gateway(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.gateway_id)
    elif args.command == 'list-gateways':
        list_gateways(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id)
    elif args.command == 'list-registries':
        list_registries(
                args.service_account_json, args.project_id,
                args.cloud_region)


def run_command(args):
    """Calls the program using the specified command."""
    if args.project_id is None:
        print('You must specify a project ID or set the environment variable.')
        return
    elif args.command.startswith('create'):
        run_create(args)
    elif args.command.startswith('get'):
        run_get(args)
    elif args.command.startswith('list'):
        run_list(args)

    elif args.command == 'bind-device-to-gateway':
        bind_device_to_gateway(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.gateway_id)
    elif args.command == 'delete-device':
        delete_device(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id)
    elif args.command == 'delete-registry':
        delete_registry(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id)
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
    elif args.command == 'send-command':
        send_command(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.send_command)
    elif args.command == 'set-iam-permissions':
        if (args.member is None):
            sys.exit('Error: specify --member')
        if (args.role is None):
            sys.exit('Error: specify --role')
        set_iam_permissions(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.role, args.member)
    elif args.command == 'set-config':
        if (args.config is None):
            sys.exit('Error: specify --config')
        if (args.version is None):
            sys.exit('Error: specify --version')
        set_config(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.version, args.config)
    elif args.command == 'unbind-device-from-gateway':
        unbind_device_from_gateway(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.gateway_id)


if __name__ == '__main__':
    args = parse_command_line_args()
    run_command(args)
