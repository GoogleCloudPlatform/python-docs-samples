# Copyright 2018 Google Inc. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Sample device that receives URLs from Google Cloud Storage to download
files that are greater than the max size allowed for configuration
updates (64 KB). The device outputs messages over MQTT. Separately, a
server runs that uploads a file to Google Cloud Storage on command.
The URL for the file in GCS is sent to the MQTT config topic,
which the device listens to. When a new URL is sent to the topic, the device
picks it up and uses the URL to download the file.

To connect the device you must have downloaded Google's CA root certificates,
and a copy of your private key file. See cloud.google.com/iot for instructions
on how to do this. Run this script with the corresponding algorithm flag.

 $ python gcs_example_device.py \
      --project_id=my-project-id \
      --registry_id=example-my-registry-id \
      --device_id=my-device-id \
      --private_key_file=rsa_private.pem \
      --algorithm=RS256

With a single server, you can run multiple instances of the device with
different device ids, and the server will distinguish them. Try creating a few
devices and running them all at the same time.
"""

import argparse
import datetime
import json
import os
import threading
import time

from google.cloud import storage
import jwt
import paho.mqtt.client as mqtt


# [START create_jwt]
def create_jwt(project_id, private_key_file, algorithm):
    """Create a JWT (https://jwt.io) to establish an MQTT connection."""
    token = {
        "iat": datetime.datetime.now(tz=datetime.timezone.utc),
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=60),
        "aud": project_id,
    }
    with open(private_key_file) as f:
        private_key = f.read()
    print(
        "Creating JWT using {} from private key file {}".format(
            algorithm, private_key_file
        )
    )
    return jwt.encode(token, private_key, algorithm=algorithm)


# [END create_jwt]


def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return f"{rc}: {mqtt.error_string(rc)}"


class Device:
    """Represents the state of a single device."""

    def __init__(self):
        self.connected_event = threading.Event()

    # [START wait_for_connection]
    def wait_for_connection(self, timeout):
        """Wait for the device to become connected."""
        # The wait() method takes an argument representing the
        # number of seconds to wait before the event times out.
        print("Device is connecting...")
        while not self.connected_event.wait(timeout):
            raise RuntimeError("Could not connect to MQTT bridge.")

    # [END wait_for_connection]

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        """Callback for when a device connects."""
        if rc != 0:
            print("Error connecting:", error_str(rc))
        else:
            print("Connected successfully.")
        self.connected_event.set()

    def on_disconnect(self, unused_client, unused_userdata, rc):
        """Callback for when a device disconnects."""
        print("Disconnected:", error_str(rc))
        self.connected_event.clear()

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        """Callback when the device receives a PUBACK from the MQTT bridge."""
        print("Published message acked.")

    def on_subscribe(self, unused_client, unused_userdata, unused_mid, granted_qos):
        """Callback when the device receives a SUBACK from the MQTT bridge."""
        if granted_qos[0] == 128:
            print("Subscription failed.")
        else:
            print("Subscribed: ", granted_qos)

    # [START on_message]
    def on_message(self, unused_client, unused_userdata, message):
        """Callback when the device receives a message on a subscription."""
        payload = str(message.payload)
        print(
            "Received message '{}' on topic '{}' with Qos {}".format(
                payload, message.topic, str(message.qos)
            )
        )

        # The device will receive its latest config when it subscribes to the
        # config topic. If there is no configuration for the device, the device
        # will receive a config with an empty payload.
        if not payload:
            return

        data = json.loads(payload)
        print("Received new config.")
        bucket_name = data["bucket_name"]
        print(f"Bucket name is: '{bucket_name}'")
        config_name = data["gcs_file_name"]
        print(f"Config name is: '{config_name}'")
        # Destination file name is a byte literal because it's a file
        # name.
        destination_file_name = data[b"destination_file_name"]

        download_blob(bucket_name, config_name, destination_file_name)

    # [END on_message]


def download_blob(bucket_name, config_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(config_name)

    blob.download_to_filename(destination_file_name)

    print(f"Config {config_name} downloaded to {destination_file_name}.")


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Example Google Cloud IoT MQTT device connection code."
    )
    parser.add_argument(
        "--project_id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        required=True,
        help="GCP cloud project name.",
    )
    parser.add_argument("--registry_id", required=True, help="Cloud IoT registry id")
    parser.add_argument("--device_id", required=True, help="Cloud IoT device id")
    parser.add_argument(
        "--private_key_file", required=True, help="Path to private key file."
    )
    parser.add_argument(
        "--algorithm",
        choices=("RS256", "ES256"),
        required=True,
        help="Which encryption algorithm to use to generate the JWT.",
    )
    parser.add_argument(
        "--cloud_region", default="us-central1", help="GCP cloud region"
    )
    parser.add_argument(
        "--ca_certs",
        default="roots.pem",
        help="CA root certificate. Get from https://pki.google.com/roots.pem",
    )
    parser.add_argument(
        "--num_messages", type=int, default=100, help="Number of messages to publish."
    )
    parser.add_argument(
        "--mqtt_bridge_hostname",
        default="mqtt.googleapis.com",
        help="MQTT bridge hostname.",
    )
    parser.add_argument("--mqtt_bridge_port", default=8883, help="MQTT bridge port.")

    return parser.parse_args()


def main():
    args = parse_command_line_args()

    # Create the MQTT client and connect to Cloud IoT.
    client = mqtt.Client(
        client_id="projects/{}/locations/{}/registries/{}/devices/{}".format(
            args.project_id, args.cloud_region, args.registry_id, args.device_id
        )
    )
    client.username_pw_set(
        username="unused",
        password=create_jwt(args.project_id, args.private_key_file, args.algorithm),
    )
    client.tls_set(ca_certs=args.ca_certs)

    device = Device()

    client.on_connect = device.on_connect
    client.on_publish = device.on_publish
    client.on_disconnect = device.on_disconnect
    client.on_subscribe = device.on_subscribe
    client.on_message = device.on_message

    client.connect(args.mqtt_bridge_hostname, args.mqtt_bridge_port)

    client.loop_start()

    # This is the topic that the device will publish telemetry events to.
    mqtt_telemetry_topic = f"/devices/{args.device_id}/events"

    # This is the topic that the device will receive configuration updates on.
    mqtt_config_topic = f"/devices/{args.device_id}/config"

    # Wait up to 5 seconds for the device to connect.
    device.wait_for_connection(5)

    # Subscribe to the config topic.
    client.subscribe(mqtt_config_topic, qos=1)

    # Publish num_messages mesages to the MQTT bridge once per second.
    for i in range(1, args.num_messages + 1):
        payload = f"{args.registry_id}/{args.device_id}-payload-{i}"
        print(f"Publishing message {i}/{args.num_messages}: '{payload}'")
        client.publish(request={"topic": mqtt_telemetry_topic, "messages": payload})
        # Send events every second.
        time.sleep(1)

    client.disconnect()
    client.loop_stop()
    print("Finished loop successfully. Goodbye!")


if __name__ == "__main__":
    main()
