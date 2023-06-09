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
r"""Sample script that pushes a large file to Google Cloud IoT Core devices.
This script, when run, creates a Cloud Storage bucket (if necessary), uploads
a file from the local file system to GCS, makes the file world-readable, and
then sends the bucket and file information to a device.

If you are running this example from a Compute Engine VM, you will have to
enable the Cloud Pub/Sub API for your project, which you can do from the Cloud
Console.

Make sure that you have a device that is accepting messages on
'/devices/{device-id}/config'. You can then run the example with:

  $ python cloudiot_send_large_file.py \
    --project_id=project-id \
    --registry_id=registry-id \
    --device_id=device-id \
    --bucket_name=bucket-name \
    --gcs_file_name=gcs-file-name \
    --service_account_json=service_account.json \
    --source_file_name=source-file-name

"""

import argparse
import base64
import json
import os

from google.cloud import storage
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def get_client(service_account_json):
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    api_version = "v1"
    discovery_api = "https://cloudiot.googleapis.com/$discovery/rest"
    service_name = "cloudiotcore"

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json
    )
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = f"{discovery_api}?version={api_version}"

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials,
    )


def create_bucket(bucket_name):
    """Creates a new bucket. Only necessary the first time the script runs."""
    storage_client = storage.Client()

    try:
        storage_client.create_bucket(bucket_name)
        print(f"Bucket {bucket_name} created")
    except BaseException:
        # If the bucket already exists, ignore the 409 HTTP error and
        # continue with the rest of the program.
        print(f"Bucket {bucket_name} already exists.")


def upload_local_file(bucket_name, gcs_file_name, source_file_name):
    """Uploads a file from the local file system to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    config = bucket.blob(gcs_file_name)

    config.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded as {gcs_file_name}.")


def make_file_public(bucket_name, gcs_file_name):
    """Makes the file publicly accessible so that a device can download it."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    config = bucket.blob(gcs_file_name)

    config.make_public()

    print(f"File {config.name} is publicly accessible at {config.public_url}")


def send_to_device(
    bucket_name,
    gcs_file_name,
    destination_file_name,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    service_account_json,
):
    """Sends the configuration to the device."""

    client = get_client(service_account_json)

    device_name = "projects/{}/locations/{}/registries/{}/devices/{}".format(
        project_id, cloud_region, registry_id, device_id
    )

    config_data = {
        "bucket_name": bucket_name,
        "gcs_file_name": gcs_file_name,
        "destination_file_name": destination_file_name,
    }

    config_data_json = json.dumps(config_data, separators=(",", ": "))

    body = {
        # The device configuration specifies a version to update, which
        # can be used to avoid having configuration updates race. In this
        # case, you use the special value of 0, which tells Cloud IoT Core to
        # always update the config.
        "version_to_update": 0,
        # The data is passed as raw bytes, so we encode it as base64. Note
        # that the device will receive the decoded string, and so you do not
        # need to base64 decode the string on the device.
        "binary_data": base64.b64encode(config_data_json.encode("utf-8")).decode(
            "ascii"
        ),
    }

    request = (
        client.projects()
        .locations()
        .registries()
        .devices()
        .modifyCloudToDeviceConfig(name=device_name, body=body)
    )

    try:
        request.execute()
        print(f"Successfully sent file to device: {device_id}")
    except HttpError as e:
        # If the server responds with an HtppError, most likely because
        # the config version sent differs from the version on the
        # device, log it here.
        print(f"Error executing ModifyCloudToDeviceConfig: {e}")


def get_state(service_account_json, project_id, cloud_region, registry_id, device_id):
    """Retrieve the device's information."""
    print("Getting device information.")
    client = get_client(service_account_json)

    device_name = "projects/{}/locations/{}/registries/{}/devices/{}".format(
        project_id, cloud_region, registry_id, device_id
    )

    devices = client.projects().locations().registries().devices()
    device = devices.get(name=device_name).execute()

    print("Id : {}".format(device.get("id")))
    print("Config:")
    print("\tdata: {}".format(device.get("config").get("data")))
    print("\tfirmware_version: {}".format(device.get("config").get("version")))
    print("\tcloudUpdateTime: {}".format(device.get("config").get("cloudUpdateTime")))


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Example of uploading a config (file) to Google Cloud "
        "Storage, then sending the bucket name and file name for the "
        "config to a Cloud IoT Core device."
    )
    # Required arguments
    parser.add_argument(
        "--project_id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        required=True,
        help="GCP project name.",
    )
    parser.add_argument(
        "--bucket_name",
        required=True,
        help="The name of the bucket containing the file.",
    )
    parser.add_argument(
        "--gcs_file_name", required=True, help="The name of the file to be sent."
    )
    parser.add_argument(
        "--source_file_name",
        required=True,
        help="The name of file on the local file system.",
    )
    parser.add_argument(
        "--destination_file_name",
        required=True,
        help="The file to write to on the device.",
    )
    parser.add_argument(
        "--registry_id", required=True, help="The registry for the device."
    )
    parser.add_argument(
        "--device_id",
        required=True,
        help="The device to which to send the config update.",
    )

    # Optional arguments
    parser.add_argument(
        "--service_account_json",
        default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        help="Path to service account json file.",
    )
    parser.add_argument("--cloud_region", default="us-central1", help="Cloud region")

    return parser.parse_args()


def main():
    args = parse_command_line_args()

    print(
        "Checking if bucket {} exists and creating it if doesn't...".format(
            args.bucket_name
        )
    )
    create_bucket(args.bucket_name)

    print(
        "Uploading file '{}' to bucket "
        "'{}'...".format(args.source_file_name, args.bucket_name)
    )

    upload_local_file(args.bucket_name, args.gcs_file_name, args.source_file_name)

    print("Making file public...")
    make_file_public(args.bucket_name, args.gcs_file_name)

    print("Sending file location to device...")
    send_to_device(
        args.bucket_name,
        args.gcs_file_name,
        args.destination_file_name,
        args.project_id,
        args.cloud_region,
        args.registry_id,
        args.device_id,
        args.service_account_json,
    )

    print("Getting information from the device after the config update...")
    get_state(
        args.service_account_json,
        args.project_id,
        args.cloud_region,
        args.registry_id,
        args.device_id,
    )


if __name__ == "__main__":
    main()
