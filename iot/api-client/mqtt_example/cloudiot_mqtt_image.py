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
import base64
import binascii
import os
import sys
import threading
import time

from google.cloud import pubsub

# Add manager as library
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "manager"))  # noqa
import cloudiot_mqtt_example  # noqa


# [START iot_mqtt_image]
def transmit_image(
    cloud_region,
    registry_id,
    device_id,
    rsa_private_path,
    ca_cert_path,
    image_path,
    project_id,
    service_account_json,
):
    """Send an inage to a device registry"""

    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    sub_topic = "events"
    mqtt_topic = f"/devices/{device_id}/{sub_topic}"

    client = cloudiot_mqtt_example.get_client(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        rsa_private_path,
        "RS256",
        ca_cert_path,
        "mqtt.googleapis.com",
        8883,
    )

    client.loop_start()
    client.publish(mqtt_topic, image_data)
    time.sleep(2)
    client.loop_stop()


# [END iot_mqtt_image]


def receive_image(project_id, subscription_path, prefix, extension, timeout):
    """Receieve images transmitted to a PubSub subscription."""
    subscriber = pubsub.SubscriberClient()

    global count
    count = 0
    file_pattern = "{}-{}.{}"

    # Set up a callback to acknowledge a message. This closes around an event
    # so that it can signal that it is done and the main thread can continue.
    job_done = threading.Event()

    def callback(message):
        global count
        try:
            count = count + 1
            print(f"Received image {count}:")
            image_data = base64.b64decode(message.data)

            with open(file_pattern.format(prefix, count, extension), "wb") as f:
                f.write(image_data)
                message.ack()
                # Signal to the main thread that we can exit.
                job_done.set()

        except binascii.Error:
            message.ack()  # To move forward if a message can't be processed

    subscriber.subscribe(subscription_path, callback=callback)

    print(f"Listening for messages on {subscription_path}")
    finished = job_done.wait(timeout=timeout)
    if not finished:
        print("No event received before the timeout.")


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=("Google Cloud IoT Core MQTT binary transmission demo.")
    )
    parser.add_argument(
        "--ca_certs",
        default="roots.pem",
        help=("CA root from https://pki.google.com/roots.pem"),
    )
    parser.add_argument(
        "--cloud_region", default="us-central1", help="GCP cloud region"
    )
    parser.add_argument(
        "--image_path",
        default="./",
        help="The telemetry data sent on behalf of a device",
    )
    parser.add_argument("--device_id", required=True, help="Cloud IoT Core device id")
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
    parser.add_argument(
        "--subscription_name", help="PubSub subscription for receieving images."
    )
    parser.add_argument(
        "--image_prefix", help="Image prefix used when receieving images."
    )
    parser.add_argument(
        "--image_extension", help="Image extension used when receiving images."
    )
    parser.add_argument(
        "--duration",
        default=60,
        type=int,
        help="Number of seconds to receieve images for.",
    )

    command = parser.add_subparsers(dest="command")
    command.add_parser("send", help=transmit_image.__doc__)
    command.add_parser("recv", help=receive_image.__doc__)
    return parser.parse_args()


def main():
    args = parse_command_line_args()

    if args.command == "send":
        transmit_image(
            args.cloud_region,
            args.registry_id,
            args.device_id,
            args.private_key_file,
            args.ca_certs,
            args.image_path,
            args.project_id,
            args.service_account_json,
        )
    elif args.command == "recv":
        receive_image(
            args.project_id,
            args.subscription_name,
            args.image_prefix,
            args.image_extension,
            args.duration,
        )
    else:
        print(args.print_help())


if __name__ == "__main__":
    main()
