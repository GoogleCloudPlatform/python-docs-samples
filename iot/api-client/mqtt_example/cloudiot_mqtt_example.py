#!/usr/bin/env python

# Copyright 2017 Google Inc.
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

"""Python sample for connecting to Google Cloud IoT Core via MQTT, using JWT.

This example connects to Google Cloud IoT Core via MQTT, using a JWT for device
authentication. After connecting, by default the device publishes 100 messages
to the device's MQTT topic at a rate of one per second, and then exits.

Before you run the sample, you must register your device as described in the
README in the parent folder.

After registering the device, download Google's CA root certificates with

    wget https://pki.google.com/roots.pem

and run this script with the corresponding algorithm flag, for example:

    python cloudiot_mqtt_example.py --project_id=my-project-id \
                                    --registry_id=my-registry-id \
                                    --device_id=my-device-id \
                                    --private_key_file=rsa_private.pem \
                                    --algorithm=RS256
"""

import argparse
import datetime
import time

import jwt
import paho.mqtt.client as mqtt


def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.

    Args:
     project_id: The cloud project ID this device belongs to

     private_key_file: A path to a file containing either an RSA256 or ES256
         private key.

     algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'

    Returns:
      An MQTT generated from the given project_id and private key, which
      expires in 20 minutes. After 20 minutes, your client will be
      disconnected, and a new JWT will have to be generated.

    Raises:
      ValueError: If the private_key_file does not contain a known key.
    """

    token = {
        # The time that the token was issued at
        'iat': datetime.datetime.utcnow(),
        # When this token expires. The device will be disconnected after the
        # token expires, and will have to reconnect.
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        # The audience field should always be set to the GCP project id.
        'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print(
            'Creating JWT using {} from private key file {}'.format(
                    algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', error_str(rc))


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=(
                'Example Google Cloud IoT Core MQTT device connection code.'))
    parser.add_argument(
            '--project_id',
            required=True,
            help='GCP cloud project name')
    parser.add_argument(
            '--registry_id',
            required=True,
            help='Cloud IoT Core registry id')
    parser.add_argument(
            '--device_id',
            required=True,
            help='Cloud IoT Core device id')
    parser.add_argument(
            '--private_key_file',
            required=True,
            help='Path to private key file.')
    parser.add_argument(
            '--algorithm',
            choices=('RS256', 'ES256'),
            required=True,
            help='Which encryption algorithm to use to generate the JWT.')
    parser.add_argument(
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--ca_certs',
            default='roots.pem',
            help=('CA root certificate from https://pki.google.com/roots.pem'))
    parser.add_argument(
            '--num_messages',
            type=int,
            default=100,
            help='Number of messages to publish.')
    parser.add_argument(
            '--mqtt_bridge_hostname',
            default='mqtt.googleapis.com',
            help='MQTT bridge hostname.')
    parser.add_argument(
            '--mqtt_bridge_port', default=8883, help='MQTT bridge port.')

    return parser.parse_args()


def main():
    args = parse_command_line_args()

    # Create our MQTT client. The client_id is a unique string that identifies
    # this device. For Google Cloud IoT Core, it must be in the format below.
    client = mqtt.Client(
            client_id=(
                    'projects/{}/locations/{}/registries/{}/devices/{}'
                    .format(
                            args.project_id, args.cloud_region,
                            args.registry_id, args.device_id)))

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
            username='unused',
            password=create_jwt(
                    args.project_id, args.private_key_file, args.algorithm))

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=args.ca_certs)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # Connect to the Google MQTT bridge.
    client.connect(args.mqtt_bridge_hostname, args.mqtt_bridge_port)

    # Start the network loop.
    client.loop_start()

    mqtt_topic = '/devices/{}/events'.format(args.device_id)

    # Publish num_messages mesages to the MQTT bridge once per second.
    for i in range(1, args.num_messages + 1):
        payload = '{}/{}-payload-{}'.format(
                args.registry_id, args.device_id, i)
        print(
                'Publishing message {}/{}: \'{}\''.format(
                        i, args.num_messages, payload))
        # Publish "payload" to the MQTT topic. qos=1 means at least once
        # delivery. Cloud IoT Core also supports qos=0 for at most once
        # delivery.
        client.publish(mqtt_topic, payload, qos=1)
        time.sleep(1)

    # End the network loop and finish.
    client.loop_stop()
    print('Finished.')


if __name__ == '__main__':
    main()
