#!/usr/bin/env python

# Copyright 2018 Google LLC
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

    python send.py \\
      --device_id=your-device-id \\
      --project_id=your-project-id \\
      --send_command="Command to send" \\
      --registry_id=your-registry-id \\
      --service_account_json=/path/to/your/service_account.json \\
      send-command

"""

import argparse
import base64
import os
import time

from google.oauth2 import service_account
from googleapiclient import discovery


def get_client(service_account_json):
    """Returns an authorized API client by discovering the IoT API using the
    provided API key and creating a service object using the service account
    credentials JSON."""
    # [START authorize]
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
            service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(discovery_api, api_version)

    return discovery.build(
            service_name,
            api_version,
            discoveryServiceUrl=discovery_url,
            credentials=scoped_credentials)
    # [END authorize]


def send_command(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        command):
    """Send a command to a device."""
    # [START send_command]
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
    # [END send_command]


if __name__ == '__main__':
    """Parse command line arguments."""
    default_registry = 'cloudiot_device_manager_example_registry_{}'.format(
            int(time.time()))

    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    # Required arguments
    parser.add_argument(
            '--registry_id',
            default=default_registry,
            required=True,
            help='Registry id. If not set, a name will be generated.')
    parser.add_argument(
            '--device_id',
            required=True,
            help='Device id.')
    parser.add_argument(
            '--send_command',
            required=True,
            help='The command sent to the device')

    # Optional arguments
    parser.add_argument(  # TODO: FIXME(class) switch to us-central1
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--project_id',
            default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            help='GCP cloud project name.')
    parser.add_argument(
            '--service_account_json',
            default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            help='Path to service account json file.')

    # Command subparser
    command = parser.add_subparsers(dest='command')

    command.add_parser('send-command', help=send_command.__doc__)

    args = parser.parse_args()

    print(args.command)
    send_command(
            args.service_account_json, args.project_id,
            args.cloud_region, args.registry_id, args.device_id,
            args.send_command)
