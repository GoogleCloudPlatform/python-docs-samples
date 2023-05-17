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
"""Python sample for connecting to Google Cloud IoT Core via MQTT, using JWT.
This example connects to Google Cloud IoT Core via MQTT, using a JWT for device
authentication. After connecting, by default the device publishes 100 messages
to the device's MQTT topic at a rate of one per second, and then exits.
Before you run the sample, you must follow the instructions in the README
for this sample.
"""

# [START iot_mqtt_includes]
import argparse
import datetime
import logging
import os
import random
import ssl
import time

import jwt
import paho.mqtt.client as mqtt

# [END iot_mqtt_includes]

logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.CRITICAL)

# The initial backoff time after a disconnection occurs, in seconds.
minimum_backoff_time = 1

# The maximum backoff time before giving up, in seconds.
MAXIMUM_BACKOFF_TIME = 32

# Whether to wait with exponential backoff before publishing.
should_backoff = False


# [START iot_mqtt_jwt]
def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
    Args:
     project_id: The cloud project ID this device belongs to
     private_key_file: A path to a file containing either an RSA256 or
             ES256 private key.
     algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
    Returns:
        A JWT generated from the given project_id and private key, which
        expires in 20 minutes. After 20 minutes, your client will be
        disconnected, and a new JWT will have to be generated.
    Raises:
        ValueError: If the private_key_file does not contain a known key.
    """

    token = {
        # The time that the token was issued at
        "iat": datetime.datetime.now(tz=datetime.timezone.utc),
        # The time the token expires.
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=20),
        # The audience field should always be set to the GCP project id.
        "aud": project_id,
    }

    # Read the private key file.
    with open(private_key_file) as f:
        private_key = f.read()

    print(
        "Creating JWT using {} from private key file {}".format(
            algorithm, private_key_file
        )
    )

    return jwt.encode(token, private_key, algorithm=algorithm)


# [END iot_mqtt_jwt]


# [START iot_mqtt_config]
def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return f"{rc}: {mqtt.error_string(rc)}"


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print("on_connect", mqtt.connack_string(rc))

    # After a successful connect, reset backoff time and stop backing off.
    global should_backoff
    global minimum_backoff_time
    should_backoff = False
    minimum_backoff_time = 1


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print("on_disconnect", error_str(rc))

    # Since a disconnect occurred, the next loop iteration will wait with
    # exponential backoff.
    global should_backoff
    should_backoff = True


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print("on_publish")


def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload.decode("utf-8"))
    print(
        "Received message '{}' on topic '{}' with Qos {}".format(
            payload, message.topic, str(message.qos)
        )
    )


def get_client(
    project_id,
    cloud_region,
    registry_id,
    device_id,
    private_key_file,
    algorithm,
    ca_certs,
    mqtt_bridge_hostname,
    mqtt_bridge_port,
):
    """Create our MQTT client. The client_id is a unique string that identifies
    this device. For Google Cloud IoT Core, it must be in the format below."""
    client_id = "projects/{}/locations/{}/registries/{}/devices/{}".format(
        project_id, cloud_region, registry_id, device_id
    )
    print(f"Device client_id is '{client_id}'")

    client = mqtt.Client(client_id=client_id)

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
        username="unused", password=create_jwt(project_id, private_key_file, algorithm)
    )

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    # This is the topic that the device will receive configuration updates on.
    mqtt_config_topic = f"/devices/{device_id}/config"

    # Subscribe to the config topic.
    client.subscribe(mqtt_config_topic, qos=1)

    # The topic that the device will receive commands on.
    mqtt_command_topic = f"/devices/{device_id}/commands/#"

    # Subscribe to the commands topic, QoS 1 enables message acknowledgement.
    print(f"Subscribing to {mqtt_command_topic}")
    client.subscribe(mqtt_command_topic, qos=0)

    return client


# [END iot_mqtt_config]


def detach_device(client, device_id):
    """Detach the device from the gateway."""
    # [START iot_detach_device]
    detach_topic = f"/devices/{device_id}/detach"
    print(f"Detaching: {detach_topic}")
    client.publish(detach_topic, "{}", qos=1)
    # [END iot_detach_device]


def attach_device(client, device_id, auth):
    """Attach the device to the gateway."""
    # [START iot_attach_device]
    attach_topic = f"/devices/{device_id}/attach"
    attach_payload = f'{{"authorization" : "{auth}"}}'
    client.publish(attach_topic, attach_payload, qos=1)
    # [END iot_attach_device]


def listen_for_messages(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    gateway_id,
    num_messages,
    private_key_file,
    algorithm,
    ca_certs,
    mqtt_bridge_hostname,
    mqtt_bridge_port,
    jwt_expires_minutes,
    duration,
    cb=None,
):
    """Listens for messages sent to the gateway and bound devices."""
    # [START iot_listen_for_messages]
    global minimum_backoff_time

    jwt_iat = datetime.datetime.now(tz=datetime.timezone.utc)
    jwt_exp_mins = jwt_expires_minutes
    # Use gateway to connect to server
    client = get_client(
        project_id,
        cloud_region,
        registry_id,
        gateway_id,
        private_key_file,
        algorithm,
        ca_certs,
        mqtt_bridge_hostname,
        mqtt_bridge_port,
    )

    attach_device(client, device_id, "")
    print("Waiting for device to attach.")
    time.sleep(5)

    # The topic devices receive configuration updates on.
    device_config_topic = f"/devices/{device_id}/config"
    client.subscribe(device_config_topic, qos=1)

    # The topic gateways receive configuration updates on.
    gateway_config_topic = f"/devices/{gateway_id}/config"
    client.subscribe(gateway_config_topic, qos=1)

    # The topic gateways receive error updates on. QoS must be 0.
    error_topic = f"/devices/{gateway_id}/errors"
    client.subscribe(error_topic, qos=0)

    # Wait for about a minute for config messages.
    for i in range(1, duration):
        client.loop()
        if cb is not None:
            cb(client)

        if should_backoff:
            # If backoff time is too large, give up.
            if minimum_backoff_time > MAXIMUM_BACKOFF_TIME:
                print("Exceeded maximum backoff time. Giving up.")
                break

            delay = minimum_backoff_time + random.randint(0, 1000) / 1000.0
            time.sleep(delay)
            minimum_backoff_time *= 2
            client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

        seconds_since_issue = (datetime.datetime.now(tz=datetime.timezone.utc) - jwt_iat).seconds
        if seconds_since_issue > 60 * jwt_exp_mins:
            print(f"Refreshing token after {seconds_since_issue}s")
            jwt_iat = datetime.datetime.now(tz=datetime.timezone.utc)
            client.loop()
            client.disconnect()
            client = get_client(
                project_id,
                cloud_region,
                registry_id,
                gateway_id,
                private_key_file,
                algorithm,
                ca_certs,
                mqtt_bridge_hostname,
                mqtt_bridge_port,
            )

        time.sleep(1)

    detach_device(client, device_id)

    print("Finished.")
    # [END iot_listen_for_messages]


def send_data_from_bound_device(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    gateway_id,
    num_messages,
    private_key_file,
    algorithm,
    ca_certs,
    mqtt_bridge_hostname,
    mqtt_bridge_port,
    jwt_expires_minutes,
    payload,
):
    """Sends data from a gateway on behalf of a device that is bound to it."""
    # [START send_data_from_bound_device]
    global minimum_backoff_time

    # Publish device events and gateway state.
    device_topic = "/devices/{}/{}".format(device_id, "state")
    gateway_topic = "/devices/{}/{}".format(gateway_id, "state")

    jwt_iat = datetime.datetime.now(tz=datetime.timezone.utc)
    jwt_exp_mins = jwt_expires_minutes
    # Use gateway to connect to server
    client = get_client(
        project_id,
        cloud_region,
        registry_id,
        gateway_id,
        private_key_file,
        algorithm,
        ca_certs,
        mqtt_bridge_hostname,
        mqtt_bridge_port,
    )

    attach_device(client, device_id, "")
    print("Waiting for device to attach.")
    time.sleep(5)

    # Publish state to gateway topic
    gateway_state = f"Starting gateway at: {time.time()}"
    print(gateway_state)
    client.publish(gateway_topic, gateway_state)

    # Publish num_messages messages to the MQTT bridge
    for i in range(1, num_messages + 1):
        client.loop()

        if should_backoff:
            # If backoff time is too large, give up.
            if minimum_backoff_time > MAXIMUM_BACKOFF_TIME:
                print("Exceeded maximum backoff time. Giving up.")
                break

            delay = minimum_backoff_time + random.randint(0, 1000) / 1000.0
            time.sleep(delay)
            minimum_backoff_time *= 2
            client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

        payload = f"{registry_id}/{gateway_id}-{device_id}-payload-{i}"

        print(
            "Publishing message {}/{}: '{}' to {}".format(
                i, num_messages, payload, device_topic
            )
        )
        client.publish(device_topic, f"{device_id} : {payload}")

        seconds_since_issue = (datetime.datetime.now(tz=datetime.timezone.utc) - jwt_iat).seconds
        if seconds_since_issue > 60 * jwt_exp_mins:
            print("Refreshing token after {}s").format(seconds_since_issue)
            jwt_iat = datetime.datetime.now(tz=datetime.timezone.utc)
            client = get_client(
                project_id,
                cloud_region,
                registry_id,
                gateway_id,
                private_key_file,
                algorithm,
                ca_certs,
                mqtt_bridge_hostname,
                mqtt_bridge_port,
            )

        time.sleep(5)

    detach_device(client, device_id)

    print("Finished.")
    # [END send_data_from_bound_device]


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=("Example Google Cloud IoT Core MQTT device connection code.")
    )
    parser.add_argument(
        "--algorithm",
        choices=("RS256", "ES256"),
        required=True,
        help="Which encryption algorithm to use to generate the JWT.",
    )
    parser.add_argument(
        "--ca_certs",
        default="roots.pem",
        help="CA root from https://pki.google.com/roots.pem",
    )
    parser.add_argument(
        "--cloud_region", default="us-central1", help="GCP cloud region"
    )
    parser.add_argument(
        "--data",
        default="Hello there",
        help="The telemetry data sent on behalf of a device",
    )
    parser.add_argument("--device_id", required=True, help="Cloud IoT Core device id")
    parser.add_argument("--gateway_id", required=False, help="Gateway identifier.")
    parser.add_argument(
        "--jwt_expires_minutes",
        default=20,
        type=int,
        help="Expiration time, in minutes, for JWT tokens.",
    )
    parser.add_argument(
        "--listen_dur",
        default=60,
        type=int,
        help="Duration (seconds) to listen for configuration messages",
    )
    parser.add_argument(
        "--message_type",
        choices=("event", "state"),
        default="event",
        help=(
            "Indicates whether the message to be published is a "
            "telemetry event or a device state message."
        ),
    )
    parser.add_argument(
        "--mqtt_bridge_hostname",
        default="mqtt.googleapis.com",
        help="MQTT bridge hostname.",
    )
    parser.add_argument(
        "--mqtt_bridge_port",
        choices=(8883, 443),
        default=8883,
        type=int,
        help="MQTT bridge port.",
    )
    parser.add_argument(
        "--num_messages", type=int, default=100, help="Number of messages to publish."
    )
    parser.add_argument(
        "--private_key_file", required=True, help="Path to private key file."
    )
    parser.add_argument(
        "--project_id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help="GCP cloud project name",
    )
    parser.add_argument(
        "--registry_id", required=True, help="Cloud IoT Core registry id"
    )
    parser.add_argument(
        "--service_account_json",
        default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        help="Path to service account json file.",
    )

    # Command subparser
    command = parser.add_subparsers(dest="command")

    command.add_parser("device_demo", help=mqtt_device_demo.__doc__)

    command.add_parser("gateway_send", help=send_data_from_bound_device.__doc__)

    command.add_parser("gateway_listen", help=listen_for_messages.__doc__)

    return parser.parse_args()


def mqtt_device_demo(args):
    """Connects a device, sends data, and receives data."""
    # [START iot_mqtt_run]
    global minimum_backoff_time
    global MAXIMUM_BACKOFF_TIME

    # Publish to the events or state topic based on the flag.
    sub_topic = "events" if args.message_type == "event" else "state"

    mqtt_topic = f"/devices/{args.device_id}/{sub_topic}"

    jwt_iat = datetime.datetime.now(tz=datetime.timezone.utc)
    jwt_exp_mins = args.jwt_expires_minutes
    client = get_client(
        args.project_id,
        args.cloud_region,
        args.registry_id,
        args.device_id,
        args.private_key_file,
        args.algorithm,
        args.ca_certs,
        args.mqtt_bridge_hostname,
        args.mqtt_bridge_port,
    )

    # Publish num_messages messages to the MQTT bridge once per second.
    for i in range(1, args.num_messages + 1):
        # Process network events.
        client.loop()

        # Wait if backoff is required.
        if should_backoff:
            # If backoff time is too large, give up.
            if minimum_backoff_time > MAXIMUM_BACKOFF_TIME:
                print("Exceeded maximum backoff time. Giving up.")
                break

            # Otherwise, wait and connect again.
            delay = minimum_backoff_time + random.randint(0, 1000) / 1000.0
            print(f"Waiting for {delay} before reconnecting.")
            time.sleep(delay)
            minimum_backoff_time *= 2
            client.connect(args.mqtt_bridge_hostname, args.mqtt_bridge_port)

        payload = f"{args.registry_id}/{args.device_id}-payload-{i}"
        print(f"Publishing message {i}/{args.num_messages}: '{payload}'")
        # [START iot_mqtt_jwt_refresh]
        seconds_since_issue = (datetime.datetime.now(tz=datetime.timezone.utc) - jwt_iat).seconds
        if seconds_since_issue > 60 * jwt_exp_mins:
            print(f"Refreshing token after {seconds_since_issue}s")
            jwt_iat = datetime.datetime.now(tz=datetime.timezone.utc)
            client.loop()
            client.disconnect()
            client = get_client(
                args.project_id,
                args.cloud_region,
                args.registry_id,
                args.device_id,
                args.private_key_file,
                args.algorithm,
                args.ca_certs,
                args.mqtt_bridge_hostname,
                args.mqtt_bridge_port,
            )
        # [END iot_mqtt_jwt_refresh]
        # Publish "payload" to the MQTT topic. qos=1 means at least once
        # delivery. Cloud IoT Core also supports qos=0 for at most once
        # delivery.
        client.publish(mqtt_topic, payload, qos=1)

        # Send events every second. State should not be updated as often
        for i in range(0, 60):
            time.sleep(1)
            client.loop()
    # [END iot_mqtt_run]


def main():
    args = parse_command_line_args()

    if args.command and args.command.startswith("gateway"):
        if args.gateway_id is None:
            print("Error: For gateway commands you must specify a gateway ID")
            return

    if args.command == "gateway_listen":
        listen_for_messages(
            args.service_account_json,
            args.project_id,
            args.cloud_region,
            args.registry_id,
            args.device_id,
            args.gateway_id,
            args.num_messages,
            args.private_key_file,
            args.algorithm,
            args.ca_certs,
            args.mqtt_bridge_hostname,
            args.mqtt_bridge_port,
            args.jwt_expires_minutes,
            args.listen_dur,
        )
        return
    elif args.command == "gateway_send":
        send_data_from_bound_device(
            args.service_account_json,
            args.project_id,
            args.cloud_region,
            args.registry_id,
            args.device_id,
            args.gateway_id,
            args.num_messages,
            args.private_key_file,
            args.algorithm,
            args.ca_certs,
            args.mqtt_bridge_hostname,
            args.mqtt_bridge_port,
            args.jwt_expires_minutes,
            args.data,
        )
        return
    else:
        mqtt_device_demo(args)
    print("Finished.")


if __name__ == "__main__":
    main()
