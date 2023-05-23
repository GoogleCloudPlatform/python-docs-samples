# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import datetime
import json
import os
import socket
import ssl
import time
from time import ctime

import jwt
import paho.mqtt.client as mqtt


# Hostname of '' means using the IP address of the machine.
HOST = ''
PORT = 10000
BUFF_SIZE = 2048
ADDR = (HOST, PORT)

udpSerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSerSock.setblocking(False)
udpSerSock.bind(ADDR)


class GatewayState:
    # This is the topic that the device will receive configuration updates on.
    mqtt_config_topic = ''

    # Host the gateway will connect to
    mqtt_bridge_hostname = ''
    mqtt_bridge_port = 8883

    # For all PUBLISH messages which are waiting for PUBACK. The key is 'mid'
    # returned by publish().
    pending_responses = {}

    # For all SUBSCRIBE messages which are waiting for SUBACK. The key is
    # 'mid'.
    pending_subscribes = {}

    # for all SUBSCRIPTIONS. The key is subscription topic.
    subscriptions = {}

    # Indicates if MQTT client is connected or not
    connected = False


gateway_state = GatewayState()


# [START iot_mqtt_jwt]
def create_jwt(project_id, private_key_file, algorithm, jwt_expires_minutes):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
            Args:
             project_id: The cloud project ID this device belongs to
             private_key_file: A path to a file containing either an RSA256 or
                             ES256 private key.
             algorithm: Encryption algorithm to use. Either 'RS256' or 'ES256'
             jwt_expires_minutes: The time in minutes before the JWT expires.
            Returns:
                An MQTT generated from the given project_id and private key,
                which expires in 20 minutes. After 20 minutes, your client will
                be disconnected, and a new JWT will have to be generated.
            Raises:
                ValueError: If the private_key_file does not contain a known
                key.
            """

    token = {
        # The time that the token was issued at
        'iat': datetime.datetime.now(tz=datetime.timezone.utc),
        # The time the token expires.
        'exp': (
            datetime.datetime.now(tz=datetime.timezone.utc) +
            datetime.timedelta(minutes=jwt_expires_minutes)),
        # The audience field should always be set to the GCP project id.
        'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file) as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)
# [END iot_mqtt_jwt]


# [START iot_mqtt_config]
def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return f'{rc}: {mqtt.error_string(rc)}'


def on_connect(client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', mqtt.connack_string(rc))

    gateway_state.connected = True

    # Subscribe to the config topic.
    client.subscribe(gateway_state.mqtt_config_topic, qos=1)


def on_disconnect(client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))
    gateway_state.connected = False

    # re-connect
    # NOTE: should implement back-off here, but it's a tutorial
    client.connect(
        gateway_state.mqtt_bridge_hostname, gateway_state.mqtt_bridge_port)


def on_publish(unused_client, userdata, mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish, userdata {}, mid {}'.format(
            userdata, mid))

    try:
        client_addr, message = gateway_state.pending_responses.pop(mid)
        udpSerSock.sendto(message.encode(), client_addr)
        print('Pending response count {}'.format(
                len(gateway_state.pending_responses)))
    except KeyError:
        print(f'Unable to find key {mid}')


def on_subscribe(unused_client, unused_userdata, mid, granted_qos):
    print(f'on_subscribe: mid {mid}, qos {granted_qos}')
    try:
        client_addr, response = gateway_state.pending_subscribes[mid]
        udpSerSock.sendto(response.encode(), client_addr)
    except KeyError:
        print(f'Unable to find mid: {mid}')


def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = message.payload
    qos = message.qos
    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload.decode("utf-8"), message.topic, qos))
    try:
        client_addr = gateway_state.subscriptions[message.topic]
        udpSerSock.sendto(payload, client_addr)
        print('Sent message to device')
    except KeyError:
        print(f'Nobody subscribes to topic {message.topic}')


def get_client(
        project_id, cloud_region, registry_id, gateway_id, private_key_file,
        algorithm, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port,
        jwt_expires_minutes):
    """Create our MQTT client. The client_id is a unique string that
    identifies this device. For Google Cloud IoT Core, it must be in the
    format below."""
    client_template = 'projects/{}/locations/{}/registries/{}/devices/{}'
    client_id = client_template.format(
        project_id, cloud_region, registry_id, gateway_id)
    client = mqtt.Client(client_id)

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
            username='unused',
            password=create_jwt(
                project_id, private_key_file, algorithm,
                jwt_expires_minutes))

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Register message callbacks.
    #     https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example,
    # the callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    return client
# [END iot_mqtt_config]


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=(
            'Example Google Cloud IoT Core MQTT device connection code.'))
    parser.add_argument(
            '--project_id',
            default=os.environ.get('GOOGLE_CLOUD_PROJECT'),
            help='GCP cloud project name')
    parser.add_argument(
            '--registry_id', required=True,
            help='Cloud IoT Core registry id')
    parser.add_argument(
            '--gateway_id', required=True,
            help='Cloud IoT Core gateway id')
    parser.add_argument(
            '--private_key_file',
            required=True, help='Path to private key file.')
    parser.add_argument(
            '--algorithm',
            choices=('RS256', 'ES256'),
            required=True,
            help='Which encryption algorithm to use to generate the JWT.')
    parser.add_argument(
            '--cloud_region', default='us-central1',
            help='GCP cloud region')
    parser.add_argument(
            '--ca_certs',
            default='roots.pem',
            help=('CA root from https://pki.google.com/roots.pem'))
    parser.add_argument(
            '--mqtt_bridge_hostname',
            default='mqtt.googleapis.com',
            help='MQTT bridge hostname.')
    parser.add_argument(
            '--mqtt_bridge_port',
            choices=(8883, 443),
            default=8883,
            type=int,
            help='MQTT bridge port.')
    parser.add_argument(
            '--jwt_expires_minutes',
            default=1200,
            type=int,
            help=('Expiration time, in minutes, for JWT tokens.'))

    return parser.parse_args()


def attach_device(client, device_id):
    attach_topic = f'/devices/{device_id}/attach'
    print(attach_topic)
    return client.publish(attach_topic,    "", qos=1)


def detatch_device(client, device_id):
    detach_topic = f'/devices/{device_id}/detach'
    print(detach_topic)
    return client.publish(detach_topic, "", qos=1)


# [START iot_mqtt_run]
def main():
    global gateway_state

    args = parse_command_line_args()

    gateway_state.mqtt_config_topic = '/devices/{}/config'.format(
        parse_command_line_args().gateway_id)
    gateway_state.mqtt_bridge_hostname = args.mqtt_bridge_hostname
    gateway_state.mqtt_bridge_port = args.mqtt_bridge_hostname

    client = get_client(
            args.project_id, args.cloud_region, args.registry_id,
            args.gateway_id, args.private_key_file, args.algorithm,
            args.ca_certs, args.mqtt_bridge_hostname, args.mqtt_bridge_port,
            args.jwt_expires_minutes)

    while True:
        client.loop()
        if gateway_state.connected is False:
            print(f'connect status {gateway_state.connected}')
            time.sleep(1)
            continue

        try:
            data, client_addr = udpSerSock.recvfrom(BUFF_SIZE)
        except OSError:
            continue
        print('[{}]: From Address {}:{} receive data: {}'.format(
                ctime(), client_addr[0], client_addr[1], data.decode("utf-8")))

        command = json.loads(data.decode('utf-8'))
        if not command:
            print(f'invalid json command {data}')
            continue

        action = command["action"]
        device_id = command["device"]
        template = '{{ "device": "{}", "command": "{}", "status" : "ok" }}'

        if action == 'event':
            print(f'Sending telemetry event for device {device_id}')
            payload = command["data"]
            mqtt_topic = f'/devices/{device_id}/events'
            print('Publishing message to topic {} with payload \'{}\''.format(
                    mqtt_topic, payload))
            _, event_mid = client.publish(mqtt_topic, payload, qos=1)
            response = template.format(device_id, 'event')
            print(f'Save mid {event_mid} for response {response}')
            gateway_state.pending_responses[event_mid] = (
                client_addr, response)
        elif action == 'attach':
            _, attach_mid = attach_device(client, device_id)
            response = template.format(device_id, 'attach')
            print(f'Save mid {attach_mid} for response {response}')
            gateway_state.pending_responses[attach_mid] = (
                client_addr, response)
        elif action == 'detach':
            _, detach_mid = detatch_device(client, device_id)
            response = template.format(device_id, 'detach')
            print(f'Save mid {detach_mid} for response {response}')
            gateway_state.pending_responses[detach_mid] = (
                client_addr, response)
        elif action == "subscribe":
            print(f'subscribe config for {device_id}')
            subscribe_topic = f'/devices/{device_id}/config'
            _, mid = client.subscribe(subscribe_topic, qos=1)
            response = template.format(device_id, 'subscribe')
            gateway_state.subscriptions[subscribe_topic] = (client_addr)
            print(f'Save mid {mid} for response {response}')
            gateway_state.pending_subscribes[mid] = (client_addr, response)
    else:
        print(f'undefined action: {action}')

    print('Finished.')
# [END iot_mqtt_run]


if __name__ == '__main__':
    main()
