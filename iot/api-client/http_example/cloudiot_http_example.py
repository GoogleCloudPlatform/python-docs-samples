#!/usr/bin/env python

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Python sample for connecting to Google Cloud IoT Core via HTTP, using JWT.
This example connects to Google Cloud IoT Core via HTTP, using a JWT for device
authentication. After connecting, by default the device publishes 100 messages
to the server at a rate of one per second, and then exits.
Before you run the sample, you must register your device as described in the
README in the parent folder.
"""

import argparse
import base64
import datetime
import json
import time

import jwt
import requests


_BASE_URL = 'https://cloudiot-device.googleapis.com/v1beta1'


def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to authenticate this device.
    Args:
     project_id: The cloud project ID this device belongs to
     private_key_file: A path to a file containing either an RSA256 or
     ES256 private key.
     algorithm: The encryption algorithm to use. Either 'RS256' or
     'ES256'
    Returns:
        A JWT generated from the given project_id and private key, which
        expires in 20 minutes. After 20 minutes, your client will be
        disconnected, and a new JWT will have to be generated.
    Raises:
        ValueError: If the private_key_file does not contain a known key.
    """

    token = {
            # The time the token was issued.
            'iat': datetime.datetime.utcnow(),
            # Token expiration time.
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
            algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)


def publish_message(
        message, message_type, base_url, project_id, cloud_region, registry_id,
        device_id, jwt_token):
    headers = {
            'authorization': 'Bearer {}'.format(jwt_token),
            'content-type': 'application/json',
            'cache-control': 'no-cache'
    }

    # Publish to the events or state topic based on the flag.
    url_suffix = 'publishEvent' if message_type == 'event' else 'setState'

    publish_url = (
        '{}/projects/{}/locations/{}/registries/{}/devices/{}:{}').format(
            base_url, project_id, cloud_region, registry_id, device_id,
            url_suffix)

    body = None
    if message_type == 'event':
        body = {'binary_data': base64.urlsafe_b64encode(message)}
    else:
        body = {
          'state': {'binary_data': base64.urlsafe_b64encode(message)}
        }

    resp = requests.post(
            publish_url, data=json.dumps(body), headers=headers)

    return resp


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=(
            'Example Google Cloud IoT Core HTTP device connection code.'))
    parser.add_argument(
            '--project_id', required=True, help='GCP cloud project name')
    parser.add_argument(
            '--registry_id', required=True, help='Cloud IoT Core registry id')
    parser.add_argument(
            '--device_id', required=True, help='Cloud IoT Core device id')
    parser.add_argument(
            '--private_key_file',
            required=True,
            help='Path to private key file.')
    parser.add_argument(
            '--algorithm',
            choices=('RS256', 'ES256'),
            required=True,
            help='The encryption algorithm to use to generate the JWT.')
    parser.add_argument(
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--ca_certs',
            default='roots.pem',
            help=('CA root from https://pki.google.com/roots.pem'))
    parser.add_argument(
            '--num_messages',
            type=int,
            default=100,
            help='Number of messages to publish.')
    parser.add_argument(
            '--message_type',
            choices=('event', 'state'),
            default='event',
            required=True,
            help=('Indicates whether the message to be published is a '
                  'telemetry event or a device state message.'))
    parser.add_argument(
            '--base_url',
            default=_BASE_URL,
            help=('Base URL for the Cloud IoT Core Device Service API'))

    return parser.parse_args()


def main():
    args = parse_command_line_args()

    jwt_token = create_jwt(
            args.project_id, args.private_key_file, args.algorithm)

    # Publish num_messages mesages to the HTTP bridge once per second.
    for i in range(1, args.num_messages + 1):
        payload = '{}/{}-payload-{}'.format(
                args.registry_id, args.device_id, i)

        print('Publishing message {}/{}: \'{}\''.format(
                i, args.num_messages, payload))

        resp = publish_message(
                payload, args.message_type, args.base_url, args.project_id,
                args.cloud_region, args.registry_id, args.device_id, jwt_token)

        print('HTTP response: ', resp)

        # Send events every second. State should not be updated as often
        time.sleep(1 if args.message_type == 'event' else 5)
    print('Finished.')


if __name__ == '__main__':
    main()
