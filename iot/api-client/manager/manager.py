#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
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
Example of using the Google Cloud IoT Core device manager to administer
devices.

Usage example:

    python manager.py \\
      --project_id=my-project-id \\
      --cloud_region=us-central1 \\
      --service_account_json=$HOME/service_account.json \\
      list-registries
"""

import argparse
import io
import os
import sys
import time

from google.api_core.exceptions import AlreadyExists
from google.cloud import iot_v1
from google.cloud import pubsub
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def create_iot_topic(project, topic_name):
    """Creates a PubSub Topic and grants access to Cloud IoT Core."""
    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project, topic_name)

    topic = pubsub_client.create_topic(topic_path)
    policy = pubsub_client.get_iam_policy(topic_path)

    policy.bindings.add(
        role="roles/pubsub.publisher",
        members=["serviceAccount:cloud-iot@system.gserviceaccount.com"],
    )

    pubsub_client.set_iam_policy(topic_path, policy)

    return topic


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

    discovery_url = "{}?version={}".format(discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials,
    )


def create_rs256_device(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    certificate_file,
):
    """Create a new device with the given id, using RS256 for
    authentication."""

    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    with io.open(certificate_file) as f:
        certificate = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        "id": device_id,
        "credentials": [{"public_key": {"format": "RSA_X509_PEM", "key": certificate}}],
    }

    return client.create_device(parent, device_template)


def create_es256_device(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    public_key_file,
):
    """Create a new device with the given id, using ES256 for
    authentication."""

    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    with io.open(public_key_file) as f:
        public_key = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        "id": device_id,
        "credentials": [{"public_key": {"format": "ES256_PEM", "key": public_key}}],
    }

    return client.create_device(parent, device_template)


def create_device(
    service_account_json, project_id, cloud_region, registry_id, device_id
):
    """Create a device to bind to a gateway if it does not exist."""

    # Check that the device doesn't already exist
    client = iot_v1.DeviceManagerClient()

    exists = False

    parent = client.registry_path(project_id, cloud_region, registry_id)

    devices = list(client.list_devices(parent=parent))

    for device in devices:
        if device.id == device_id:
            exists = True

    # Create the device
    device_template = {
        "id": device_id,
        "gateway_config": {
            "gateway_type": "NON_GATEWAY",
            "gateway_auth_method": "ASSOCIATION_ONLY",
        },
    }

    if not exists:
        res = client.create_device(parent, device_template)
        print("Created Device {}".format(res))
    else:
        print("Device exists, skipping")


def create_unauth_device(
    service_account_json, project_id, cloud_region, registry_id, device_id
):
    """Create a new device without authentication."""
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    device_template = {
        "id": device_id,
    }

    return client.create_device(parent, device_template)


def delete_device(
    service_account_json, project_id, cloud_region, registry_id, device_id
):
    """Delete the device with the given id."""
    print("Delete device")
    client = iot_v1.DeviceManagerClient()

    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    return client.delete_device(device_path)


def delete_registry(service_account_json, project_id, cloud_region, registry_id):
    """Deletes the specified registry."""
    print("Delete registry")

    client = iot_v1.DeviceManagerClient()
    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    try:
        client.delete_device_registry(registry_path)
        print("Deleted registry")
        return "Registry deleted"
    except HttpError:
        print("Error, registry not deleted")
        raise


def get_device(service_account_json, project_id, cloud_region, registry_id, device_id):
    print("Getting device")
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    device = client.get_device(device_path)

    print("Id : {}".format(device.id))
    print("Name : {}".format(device.name))
    print("Credentials:")

    if device.credentials is not None:
        for credential in device.credentials:
            keyinfo = credential.public_key
            print("\tcertificate: \n{}".format(keyinfo.key))

            if keyinfo.format == 4:
                keyformat = "ES256_X509_PEM"
            elif keyinfo.format == 3:
                keyformat = "RSA_PEM"
            elif keyinfo.format == 2:
                keyformat = "ES256_PEM"
            elif keyinfo.format == 1:
                keyformat = "RSA_X509_PEM"
            else:
                keyformat = "UNSPECIFIED_PUBLIC_KEY_FORMAT"
            print("\tformat : {}".format(keyformat))
            print("\texpiration: {}".format(credential.expiration_time))

    print("Config:")
    print("\tdata: {}".format(device.config.binary_data))
    print("\tversion: {}".format(device.config.version))
    print("\tcloudUpdateTime: {}".format(device.config.cloud_update_time))

    return device


def get_state(service_account_json, project_id, cloud_region, registry_id, device_id):
    """Retrieve a device's state blobs."""
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    device = client.get_device(device_path)
    print("Last state: {}".format(device.state))

    print("State history")
    states = client.list_device_states(device_path).device_states
    for state in states:
        print("State: {}".format(state))

    return states


def list_devices(service_account_json, project_id, cloud_region, registry_id):
    """List all devices in the registry."""
    print("Listing devices")

    client = iot_v1.DeviceManagerClient()
    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    devices = list(client.list_devices(parent=registry_path))
    for device in devices:
        print("Device: {} : {}".format(device.num_id, device.id))

    return devices


def list_registries(service_account_json, project_id, cloud_region):
    """List all registries in the project."""
    print("Listing Registries")
    client = iot_v1.DeviceManagerClient()
    parent = client.location_path(project_id, cloud_region)

    registries = list(client.list_device_registries(parent))
    for registry in registries:
        print("id: {}\n\tname: {}".format(registry.id, registry.name))

    return registries


def create_registry(
    service_account_json, project_id, cloud_region, pubsub_topic, registry_id
):
    """ Creates a registry and returns the result. Returns an empty result if
    the registry already exists."""
    client = iot_v1.DeviceManagerClient()
    parent = client.location_path(project_id, cloud_region)

    if not pubsub_topic.startswith("projects/"):
        pubsub_topic = "projects/{}/topics/{}".format(project_id, pubsub_topic)

    body = {
        "event_notification_configs": [{"pubsub_topic_name": pubsub_topic}],
        "id": registry_id,
    }

    try:
        response = client.create_device_registry(parent, body)
        print("Created registry")
        return response
    except HttpError:
        print("Error, registry not created")
        raise
    except AlreadyExists:
        print("Error, registry already exists")
        raise


def get_registry(service_account_json, project_id, cloud_region, registry_id):
    """ Retrieves a device registry."""
    client = iot_v1.DeviceManagerClient()
    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    return client.get_device_registry(registry_path)


def open_registry(
    service_account_json, project_id, cloud_region, pubsub_topic, registry_id
):
    """Gets or creates a device registry."""
    print("Creating registry")

    try:
        response = create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic, registry_id
        )
    except AlreadyExists:
        # Device registry already exists. We just re-use the existing one.
        print("Registry {} already exists - looking it up instead.".format(registry_id))
        response = get_registry(
            service_account_json, project_id, cloud_region, registry_id
        )

    print("Registry {} opened: ".format(response.name))
    print(response)


def patch_es256_auth(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    public_key_file,
):
    """Patch the device to add an ES256 public key to the device."""
    print("Patch device with ES256 certificate")

    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    public_key_bytes = ""
    with io.open(public_key_file) as f:
        public_key_bytes = f.read()

    key = iot_v1.types.PublicKeyCredential(format="ES256_PEM", key=public_key_bytes)

    cred = iot_v1.types.DeviceCredential(public_key=key)
    device = client.get_device(device_path)

    device.id = b""
    device.num_id = 0
    device.credentials.append(cred)

    mask = iot_v1.types.FieldMask()
    mask.paths.append("credentials")

    return client.update_device(device=device, update_mask=mask)


def patch_rsa256_auth(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    public_key_file,
):
    """Patch the device to add an RSA256 public key to the device."""
    print("Patch device with RSA256 certificate")

    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    public_key_bytes = ""
    with io.open(public_key_file) as f:
        public_key_bytes = f.read()

    key = iot_v1.types.PublicKeyCredential(format="RSA_X509_PEM", key=public_key_bytes)

    cred = iot_v1.types.DeviceCredential(public_key=key)
    device = client.get_device(device_path)

    device.id = b""
    device.num_id = 0
    device.credentials.append(cred)

    mask = iot_v1.types.FieldMask()
    mask.paths.append("credentials")

    return client.update_device(device=device, update_mask=mask)


def set_config(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    version,
    config,
):
    print("Set device configuration")
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    data = config.encode("utf-8")

    return client.modify_cloud_to_device_config(device_path, data, version)


def get_config_versions(
    service_account_json, project_id, cloud_region, registry_id, device_id
):
    """Lists versions of a device config in descending order (newest first)."""
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    configs = client.list_device_config_versions(device_path)

    for config in configs.device_configs:
        print(
            "version: {}\n\tcloudUpdateTime: {}\n\t data: {}".format(
                config.version, config.cloud_update_time, config.binary_data
            )
        )

    return configs


def get_iam_permissions(service_account_json, project_id, cloud_region, registry_id):
    """Retrieves IAM permissions for the given registry."""
    client = iot_v1.DeviceManagerClient()

    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    policy = client.get_iam_policy(registry_path)

    return policy


def set_iam_permissions(
    service_account_json, project_id, cloud_region, registry_id, role, member
):
    """Sets IAM permissions for the given registry to a single role/member."""
    client = iot_v1.DeviceManagerClient()
    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    body = {"bindings": [{"members": [member], "role": role}]}

    return client.set_iam_policy(registry_path, body)


def send_command(
    service_account_json, project_id, cloud_region, registry_id, device_id, command
):
    """Send a command to a device."""
    print("Sending command to device")
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    # command = 'Hello IoT Core!'
    data = command.encode("utf-8")

    return client.send_command_to_device(device_path, data)


def create_gateway(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    gateway_id,
    certificate_file,
    algorithm,
):
    """Create a gateway to bind devices to."""
    exists = False
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)
    devices = list(client.list_devices(parent=parent))

    for device in devices:
        if device.id == gateway_id:
            exists = True
        print(
            "Device: {} : {} : {} : {}".format(
                device.id, device.num_id, device.config, device.gateway_config
            )
        )

    with io.open(certificate_file) as f:
        certificate = f.read()

    if algorithm == "ES256":
        certificate_format = "ES256_PEM"
    else:
        certificate_format = "RSA_X509_PEM"

    # TODO: Auth type
    device_template = {
        "id": gateway_id,
        "credentials": [
            {"public_key": {"format": certificate_format, "key": certificate}}
        ],
        "gateway_config": {
            "gateway_type": "GATEWAY",
            "gateway_auth_method": "ASSOCIATION_ONLY",
        },
    }

    if not exists:
        res = client.create_device(parent, device_template)
        print("Created Gateway {}".format(res))
    else:
        print("Gateway exists, skipping")


def bind_device_to_gateway(
    service_account_json, project_id, cloud_region, registry_id, device_id, gateway_id
):
    """Binds a device to a gateway."""
    client = iot_v1.DeviceManagerClient()

    create_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    parent = client.registry_path(project_id, cloud_region, registry_id)

    res = client.bind_device_to_gateway(parent, gateway_id, device_id)

    print("Device Bound! {}".format(res))


def unbind_device_from_gateway(
    service_account_json, project_id, cloud_region, registry_id, device_id, gateway_id
):
    """Unbinds a device to a gateway."""
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    res = client.unbind_device_from_gateway(parent, gateway_id, device_id)

    print("Device unbound: {}".format(res))


def list_gateways(service_account_json, project_id, cloud_region, registry_id):
    """Lists gateways in a registry"""
    client = iot_v1.DeviceManagerClient()

    path = client.registry_path(project_id, cloud_region, registry_id)
    mask = iot_v1.types.FieldMask()
    mask.paths.append("config")
    mask.paths.append("gateway_config")
    devices = list(client.list_devices(parent=path, field_mask=mask))

    for device in devices:
        if device.gateway_config is not None:
            if device.gateway_config.gateway_type == 1:
                print("Gateway ID: {}\n\t{}".format(device.id, device))


def list_devices_for_gateway(
    service_account_json, project_id, cloud_region, registry_id, gateway_id
):
    """List devices bound to a gateway"""
    client = iot_v1.DeviceManagerClient()

    path = client.registry_path(project_id, cloud_region, registry_id)

    devices = list(
        client.list_devices(
            parent=path, gateway_list_options={"associations_gateway_id": gateway_id}
        )
    )

    found = False
    for device in devices:
        found = True
        print("Device: {} : {}".format(device.num_id, device.id))

    if not found:
        print("No devices bound to gateway {}".format(gateway_id))
