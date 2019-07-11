# Copyright 2019 Google Inc. All Rights Reserved.
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
import sys
import time

from google.cloud import pubsub

# Add manager as library
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'manager'))  # noqa
import manager
import cloudiot_mqtt_example


def transmit_image(
        cloud_region, registry_id, device_id, rsa_private_path, ca_cert_path,
        image_path):
    """Send an inage to a device registry"""

    with open(image_path, "rb") as f:
        data = f.read()
        image_data = data.encode("base64")

    project_id = os.environ['GCLOUD_PROJECT']
    service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

    sub_topic = 'events'
    mqtt_topic = '/devices/{}/{}'.format(device_id, sub_topic)

    client = cloudiot_mqtt_example.get_client(
        project_id, cloud_region, registry_id, device_id,
        rsa_private_path, 'RS256', ca_cert_path,
        'mqtt.googleapis.com', 8883)

    client.loop_start()
    client.publish(mqtt_topic, image_data, qos=1)
    time.sleep(2)
    client.loop_stop()

def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=(
            'Google Cloud IoT Core MQTT binary transmission demo.'))
    #parser.add_argument(
    #        '--algorithm',
    #        choices=('RS256', 'ES256'),
    #        required=True,
    #        help='Which encryption algorithm to use to generate the JWT.')
    parser.add_argument(
            '--ca_certs',
            default='roots.pem',
            help=('CA root from https://pki.google.com/roots.pem'))
    parser.add_argument(
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--image_path',
            default='./',
            help='The telemetry data sent on behalf of a device')
    parser.add_argument(
            '--device_id', required=True, help='Cloud IoT Core device id')
    #parser.add_argument(
    #        '--gateway_id', required=False, help='Gateway identifier.')
    #parser.add_argument(
    #        '--jwt_expires_minutes',
    #        default=20,
    #        type=int,
    #        help=('Expiration time, in minutes, for JWT tokens.'))
    #parser.add_argument(
    #        '--listen_dur',
    #        default=60,
    #        type=int,
    #        help='Duration (seconds) to listen for configuration messages')
    #parser.add_argument(
    #        '--message_type',
    #        choices=('event', 'state'),
    #        default='event',
    #        help=('Indicates whether the message to be published is a '
    #              'telemetry event or a device state message.'))
    #parser.add_argument(
    #        '--mqtt_bridge_hostname',
    #        default='mqtt.googleapis.com',
    #        help='MQTT bridge hostname.')
    #parser.add_argument(
    #        '--mqtt_bridge_port',
    #        choices=(8883, 443),
    #        default=8883,
    #        type=int,
    #        help='MQTT bridge port.')
    parser.add_argument(
            '--private_key_file',
            required=True,
            help='Path to private key file.')
    parser.add_argument(
            '--project_id',
            default=os.environ.get('GOOGLE_CLOUD_PROJECT'),
            help='GCP cloud project name')
    parser.add_argument(
            '--registry_id', required=True, help='Cloud IoT Core registry id')
    parser.add_argument(
            '--service_account_json',
            default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            help='Path to service account json file.')

    command = parser.add_subparsers(dest='command')
    command.add_parser(
        'send',
        help=transmit_image.__doc__)
    return parser.parse_args()


#if __name__ == '__main__':
#    main()
#def main() ...
args = parse_command_line_args()

if args.command == 'send':
    transmit_image(
        args.cloud_region, args.registry_id, args.device_id,
        args.private_key_file, args.ca_certs, args.image_path)
else:
    args.print_help()
