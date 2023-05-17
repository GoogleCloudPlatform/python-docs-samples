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

# [START iot_http_includes]
import argparse
import base64
import datetime
import json
import time

from google.api_core import retry
import jwt
import requests

# [END iot_http_includes]

_BASE_URL = "https://cloudiotdevice.googleapis.com/v1"
_BACKOFF_DURATION = 60


# [START iot_http_jwt]
def create_jwt(project_id, private_key_file, algorithm):
    token = {
        # The time the token was issued.
        "iat": datetime.datetime.now(tz=datetime.timezone.utc),
        # Token expiration time.
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=60),
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


# [END iot_http_jwt]


@retry.Retry(
    predicate=retry.if_exception_type(AssertionError), deadline=_BACKOFF_DURATION
)
# [START iot_http_publish]
def publish_message(
    message,
    message_type,
    base_url,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    jwt_token,
):
    headers = {
        "authorization": f"Bearer {jwt_token}",
        "content-type": "application/json",
        "cache-control": "no-cache",
    }

    # Publish to the events or state topic based on the flag.
    url_suffix = "publishEvent" if message_type == "event" else "setState"

    publish_url = ("{}/projects/{}/locations/{}/registries/{}/devices/{}:{}").format(
        base_url, project_id, cloud_region, registry_id, device_id, url_suffix
    )

    body = None
    msg_bytes = base64.urlsafe_b64encode(message.encode("utf-8"))
    if message_type == "event":
        body = {"binary_data": msg_bytes.decode("ascii")}
    else:
        body = {"state": {"binary_data": msg_bytes.decode("ascii")}}

    resp = requests.post(publish_url, data=json.dumps(body), headers=headers)

    if resp.status_code != 200:
        print(f"Response came back {resp.status_code}, retrying")
        raise AssertionError(f"Not OK response: {resp.status_code}")

    return resp


# [END iot_http_publish]


@retry.Retry(
    predicate=retry.if_exception_type(AssertionError), deadline=_BACKOFF_DURATION
)
# [START iot_http_getconfig]
def get_config(
    version,
    message_type,
    base_url,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    jwt_token,
):
    headers = {
        "authorization": f"Bearer {jwt_token}",
        "content-type": "application/json",
        "cache-control": "no-cache",
    }

    basepath = "{}/projects/{}/locations/{}/registries/{}/devices/{}/"
    template = basepath + "config?local_version={}"
    config_url = template.format(
        base_url, project_id, cloud_region, registry_id, device_id, version
    )

    resp = requests.get(config_url, headers=headers)

    if resp.status_code != 200:
        print(f"Error getting config: {resp.status_code}, retrying")
        raise AssertionError(f"Not OK response: {resp.status_code}")

    return resp


# [END iot_http_getconfig]


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=("Example Google Cloud IoT Core HTTP device connection code.")
    )
    parser.add_argument("--project_id", required=True, help="GCP cloud project name")
    parser.add_argument(
        "--registry_id", required=True, help="Cloud IoT Core registry id"
    )
    parser.add_argument("--device_id", required=True, help="Cloud IoT Core device id")
    parser.add_argument(
        "--private_key_file", required=True, help="Path to private key file."
    )
    parser.add_argument(
        "--algorithm",
        choices=("RS256", "ES256"),
        required=True,
        help="The encryption algorithm to use to generate the JWT.",
    )
    parser.add_argument(
        "--cloud_region", default="us-central1", help="GCP cloud region"
    )
    parser.add_argument(
        "--ca_certs",
        default="roots.pem",
        help=("CA root from https://pki.google.com/roots.pem"),
    )
    parser.add_argument(
        "--num_messages", type=int, default=100, help="Number of messages to publish."
    )
    parser.add_argument(
        "--message_type",
        choices=("event", "state"),
        default="event",
        required=True,
        help=(
            "Indicates whether the message to be published is a "
            "telemetry event or a device state message."
        ),
    )
    parser.add_argument(
        "--base_url",
        default=_BASE_URL,
        help=("Base URL for the Cloud IoT Core Device Service API"),
    )
    parser.add_argument(
        "--jwt_expires_minutes",
        default=20,
        type=int,
        help=("Expiration time, in minutes, for JWT tokens."),
    )

    return parser.parse_args()


# [START iot_http_run]
def main():
    args = parse_command_line_args()

    jwt_token = create_jwt(args.project_id, args.private_key_file, args.algorithm)
    jwt_iat = datetime.datetime.now(tz=datetime.timezone.utc)
    jwt_exp_mins = args.jwt_expires_minutes

    print(
        "Latest configuration: {}".format(
            get_config(
                "0",
                args.message_type,
                args.base_url,
                args.project_id,
                args.cloud_region,
                args.registry_id,
                args.device_id,
                jwt_token,
            ).text
        )
    )

    # Publish num_messages mesages to the HTTP bridge once per second.
    for i in range(1, args.num_messages + 1):
        seconds_since_issue = (datetime.datetime.now(tz=datetime.timezone.utc) - jwt_iat).seconds
        if seconds_since_issue > 60 * jwt_exp_mins:
            print("Refreshing token after {}s").format(seconds_since_issue)
            jwt_token = create_jwt(
                args.project_id, args.private_key_file, args.algorithm
            )
            jwt_iat = datetime.datetime.now(tz=datetime.timezone.utc)

        payload = f"{args.registry_id}/{args.device_id}-payload-{i}"

        print(f"Publishing message {i}/{args.num_messages}: '{payload}'")

        resp = publish_message(
            payload,
            args.message_type,
            args.base_url,
            args.project_id,
            args.cloud_region,
            args.registry_id,
            args.device_id,
            jwt_token,
        )

        print("HTTP response: ", resp)

        # Send events every second. State should not be updated as often
        time.sleep(1 if args.message_type == "event" else 5)
    print("Finished.")


# [END iot_http_run]


if __name__ == "__main__":
    main()
