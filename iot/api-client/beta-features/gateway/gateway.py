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
Example of using the Google Cloud IoT Core device manager to send telemetry
messages on behalf of other devices.

Usage example:

    python gateway.py \\
      --device_id=bound-device-id \\
      --gateway_id=your-gateway-id \\
      --project_id=your-project-id \\
      --data="optional telemetry data" \\
      --registry_id=your-registry-id \\
      --service_account_json=/path/to/your/service_account.json \\
      create_gateway

"""

import argparse
import datetime
import io
import os
import random
import re
import ssl
import time

from google.oauth2 import service_account
from googleapiclient import discovery

# [START iot_gateway_mqtt_includes]
# For sending telemetry and receiving commands
import jwt
import paho.mqtt.client as mqtt
# [END iot_gateway_mqtt_includes]

# [START iot_gateway_mqtt_variables]
# The initial backoff time after a disconnection occurs, in seconds.
minimum_backoff_time = 1

# The maximum backoff time before giving up, in seconds.
MAXIMUM_BACKOFF_TIME = 32

# Whether to wait with exponential backoff before publishing.
should_backoff = False

mqtt_bridge_hostname = 'mqtt.googleapis.com'
mqtt_bridge_port = 8883
# [END iot_gateway_mqtt_variables]


# [START iot_mqtt_jwt]
def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
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
            # The time the token expires.
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
# [END iot_mqtt_jwt]


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


def create_gateway(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        gateway_id, certificate_file, algorithm):
    # [START create_gateway]
    """Create a gateway to bind devices to."""
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


def create_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Create a device to bind to a gateway."""
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

    for device in devices.get('devices', []):
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
        print('No devices bound to gateway {}'.format(gateway_id))
    # [END list_devices_for_gateway]


# [START iot_mqtt_config]
def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', mqtt.connack_string(rc))

    # After a successful connect, reset backoff time and stop backing off.
    global should_backoff
    global minimum_backoff_time
    should_backoff = False
    minimum_backoff_time = 1


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))

    # Since a disconnect occurred, the next loop iteration will wait with
    # exponential backoff.
    global should_backoff
    should_backoff = True


def on_subscribe(
        unused_client, unused_userdata, unused_mid, unused_granted_qos):
    """Paho callback when client subscribes to a topic.."""
    print('on_subscribe')


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')


def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload)
    messageType = 'message'
    if(re.match(
            r'/devices/[A-Za-z0-9_-]+/errors', message.topic, re.M | re.I)):
        messageType = 'ERROR ' + messageType
    print('Received {} \'{}\' on topic \'{}\' with Qos {}'.format(
        messageType, payload, message.topic, str(message.qos)))


def get_mqtt_client(
        project_id, cloud_region, registry_id, gateway_id,
        private_key_file, algorithm, ca_certs, mqtt_bridge_hostname,
        mqtt_bridge_port):
    """Create our MQTT client. The client_id is a unique string that identifies
    this device. For Google Cloud IoT Core, it must be in the format below."""
    client = mqtt.Client(
            client_id=('projects/{}/locations/{}/registries/{}/devices/{}'
                       .format(
                               project_id,
                               cloud_region,
                               registry_id,
                               gateway_id)))

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
            username='unused',
            password=create_jwt(
                    project_id, private_key_file, algorithm))

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    return client
# [END iot_mqtt_config]


def detach_device(client, device_id):
    """Detach the device from the gateway."""
    # [START detach_device]
    detach_topic = '/devices/{}/detach'.format(device_id)
    print('Detaching: {}'.format(detach_topic))
    client.loop()
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)
    client.publish(detach_topic, '{}', qos=1)
    time.sleep(5)  # wait for the server to respond / will trigger callback
    # [END detach_device]


def attach_device(client, device_id):
    """Attach the device to the gateway."""
    # [START attach_device]
    attach_topic = '/devices/{}/attach'.format(device_id)
    print('Attaching: {}'.format(attach_topic))
    # TODO {'authorization': '<JWT_TOKEN>'}
    attach_payload = '{}'
    client.loop()
    client.publish(attach_topic, attach_payload, qos=1)
    time.sleep(5)
    # [END attach_device]


def listen_for_config_and_error_messages(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        gateway_id, num_messages, private_key_file, algorithm, ca_certs,
        mqtt_bridge_hostname, mqtt_bridge_port, jwt_expires_minutes, duration,
        cb=None):
    """Listens for configuration and system error messages on the gateway and
    bound devices."""
    # [START listen_for_config_messages]
    global minimum_backoff_time

    jwt_iat = datetime.datetime.utcnow()
    jwt_exp_mins = jwt_expires_minutes
    # Use gateway to connect to server
    client = get_mqtt_client(
        project_id, cloud_region, registry_id, gateway_id,
        private_key_file, algorithm, ca_certs, mqtt_bridge_hostname,
        mqtt_bridge_port)

    attach_device(client, device_id)
    print('Waiting for device to attach.')
    time.sleep(5)

    # The topic devices receive configuration updates on.
    device_config_topic = '/devices/{}/config'.format(device_id)
    client.subscribe(device_config_topic, qos=1)

    # The topic gateways receive configuration updates on.
    gateway_config_topic = '/devices/{}/config'.format(gateway_id)
    client.subscribe(gateway_config_topic, qos=1)

    # The topic gateways receive error updates on. QoS must be 0.
    error_topic = '/devices/{}/errors'.format(gateway_id)
    client.subscribe(error_topic, qos=0)

    # Wait for about a minute for config messages.
    for i in range(1, duration):
        client.loop()
        if cb is not None:
            cb(client)

        if should_backoff:
            # If backoff time is too large, give up.
            if minimum_backoff_time > MAXIMUM_BACKOFF_TIME:
                print('Exceeded maximum backoff time. Giving up.')
                break

            delay = minimum_backoff_time + random.randint(0, 1000) / 1000.0
            time.sleep(delay)
            minimum_backoff_time *= 2
            client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

        seconds_since_issue = (datetime.datetime.utcnow() - jwt_iat).seconds
        if seconds_since_issue > 60 * jwt_exp_mins:
            print('Refreshing token after {}s').format(seconds_since_issue)
            jwt_iat = datetime.datetime.utcnow()
            client = get_mqtt_client(
                project_id, cloud_region, registry_id, gateway_id,
                private_key_file, algorithm, ca_certs, mqtt_bridge_hostname,
                mqtt_bridge_port)

        time.sleep(1)

    detach_device(client, device_id)

    print('Finished.')
    # [END listen_for_config_messages]


def send_data_from_bound_device(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        gateway_id, num_messages, private_key_file, algorithm, ca_certs,
        mqtt_bridge_hostname, mqtt_bridge_port, jwt_expires_minutes, payload):
    """Sends data from a gateway on behalf of a device that is bound to it."""
    # [START send_data_from_bound_device]
    global minimum_backoff_time

    # Publish device events and gateway state.
    device_topic = '/devices/{}/{}'.format(device_id, 'state')
    gateway_topic = '/devices/{}/{}'.format(gateway_id, 'state')

    jwt_iat = datetime.datetime.utcnow()
    jwt_exp_mins = jwt_expires_minutes
    # Use gateway to connect to server
    client = get_mqtt_client(
        project_id, cloud_region, registry_id, gateway_id,
        private_key_file, algorithm, ca_certs, mqtt_bridge_hostname,
        mqtt_bridge_port)

    attach_device(client, device_id)
    print('Waiting for device to attach.')
    time.sleep(5)

    # Publish state to gateway topic
    gateway_state = 'Starting HUB at: {}'.format(time.time())
    print(gateway_state)
    client.publish(gateway_topic, gateway_state, qos=1)

    # Publish num_messages mesages to the MQTT bridge
    for i in range(1, num_messages + 1):
        client.loop()

        if should_backoff:
            # If backoff time is too large, give up.
            if minimum_backoff_time > MAXIMUM_BACKOFF_TIME:
                print('Exceeded maximum backoff time. Giving up.')
                break

            delay = minimum_backoff_time + random.randint(0, 1000) / 1000.0
            time.sleep(delay)
            minimum_backoff_time *= 2
            client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

        payload = '{}/{}-{}-payload-{}'.format(
                registry_id, gateway_id, device_id, i)

        print('Publishing message {}/{}: \'{}\' to {}'.format(
                i, num_messages, payload, device_topic))
        client.publish(
                device_topic, '{} : {}'.format(device_id, payload), qos=1)

        seconds_since_issue = (datetime.datetime.utcnow() - jwt_iat).seconds
        if seconds_since_issue > 60 * jwt_exp_mins:
            print('Refreshing token after {}s').format(seconds_since_issue)
            jwt_iat = datetime.datetime.utcnow()
            client = get_mqtt_client(
                project_id, cloud_region, registry_id, gateway_id,
                private_key_file, algorithm, ca_certs, mqtt_bridge_hostname,
                mqtt_bridge_port)

        time.sleep(5)

    detach_device(client, device_id)

    print('Finished.')
    # [END send_data_from_bound_device]


def parse_command_line_args():
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
            help='Device identifier.')
    parser.add_argument(
            '--gateway_id',
            required=True,
            help='Gateway identifier.')

    # Optional arguments
    parser.add_argument(
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--data',
            default='Hello there',
            help='The telemetry data sent on behalf of a device')
    parser.add_argument(
            '--project_id',
            default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            help='GCP cloud project name.')
    parser.add_argument(
            '--service_account_json',
            default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            help='Path to service account json file.')

    parser.add_argument(
            '--jwt_expires_minutes',
            default=60,
            help='Expiration time (in minutes) for JWT tokens.')
    parser.add_argument(
            '--listen_dur',
            default=60,
            help='Duration (seconds) to listen for configuration messages')
    parser.add_argument(
            '--certificate_path',
            help='Path to public certificate.')
    parser.add_argument(
            '--num_messages',
            default=10,
            type=int,
            help='Number of messages to send.')
    parser.add_argument(
            '--private_key_file',
            help='Path to private key file.')
    parser.add_argument(
            '--ca_certs',
            default='roots.pem',
            help=('CA root from https://pki.google.com/roots.pem'))
    parser.add_argument(
            '--algorithm',
            choices=('RS256', 'ES256'),
            help='Which encryption algorithm to use to generate the JWT.')

    # Command subparser
    command = parser.add_subparsers(dest='command')

    command.add_parser(
        'create_gateway',
        help=create_gateway.__doc__)

    command.add_parser(
        'bind_device_to_gateway',
        help=bind_device_to_gateway.__doc__)

    command.add_parser(
        'unbind_device_from_gateway',
        help=unbind_device_from_gateway.__doc__)

    command.add_parser(
        'list_devices_for_gateway',
        help=list_devices_for_gateway.__doc__)

    command.add_parser(
        'list_gateways',
        help=list_gateways.__doc__)

    command.add_parser(
        'send_data_from_bound_device',
        help=send_data_from_bound_device.__doc__)

    command.add_parser(
        'listen_for_config_messages',
        help=listen_for_config_and_error_messages.__doc__)

    return parser.parse_args()


def run_command(args):
    """Calls the program using the specified command."""
    if args.command == 'create_gateway':
        create_gateway(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.gateway_id, args.certificate_path, args.algorithm)
    elif args.command == 'bind_device_to_gateway':
        bind_device_to_gateway(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.gateway_id)
    elif args.command == 'unbind_device_from_gateway':
        unbind_device_from_gateway(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.gateway_id)
    elif args.command == 'list_gateways':
        list_gateways(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id)
    elif args.command == 'list_devices_for_gateway':
        list_devices_for_gateway(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.gateway_id)
    elif args.command == 'listen_for_config_messages':
        listen_for_config_and_error_messages(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.gateway_id, args.num_messages, args.private_key_file,
                args.algorithm, args.ca_certs, mqtt_bridge_hostname,
                mqtt_bridge_port, args.jwt_expires_minutes, args.listen_dur)
    elif args.command == 'send_data_from_bound_device':
        send_data_from_bound_device(
                args.service_account_json, args.project_id,
                args.cloud_region, args.registry_id, args.device_id,
                args.gateway_id, args.num_messages, args.private_key_file,
                args.algorithm, args.ca_certs, mqtt_bridge_hostname,
                mqtt_bridge_port, args.jwt_expires_minutes, args.data)


if __name__ == '__main__':
    args = parse_command_line_args()
    run_command(args)
