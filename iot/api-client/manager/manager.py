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
from google.protobuf import field_mask_pb2 as gp_field_mask
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def create_iot_topic(project, topic_name):
    """Creates a PubSub Topic and grants access to Cloud IoT Core."""
    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project, topic_name)

    topic = pubsub_client.create_topic(request={"name": topic_path})
    policy = pubsub_client.get_iam_policy(request={"resource": topic_path})

    policy.bindings.add(
        role="roles/pubsub.publisher",
        members=["serviceAccount:cloud-iot@system.gserviceaccount.com"],
    )

    pubsub_client.set_iam_policy(request={"resource": topic_path, "policy": policy})

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
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    with io.open(certificate_file) as f:
        certificate = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        "id": device_id,
        "credentials": [
            {
                "public_key": {
                    "format": iot_v1.PublicKeyFormat.RSA_X509_PEM,
                    "key": certificate,
                }
            }
        ],
    }

    return client.create_device(request={"parent": parent, "device": device_template})


def create_es256_device(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    public_key_file,
):
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    with io.open(public_key_file) as f:
        public_key = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        "id": device_id,
        "credentials": [
            {
                "public_key": {
                    "format": iot_v1.PublicKeyFormat.ES256_PEM,
                    "key": public_key,
                }
            }
        ],
    }

    return client.create_device(request={"parent": parent, "device": device_template})


def create_device(
    service_account_json, project_id, cloud_region, registry_id, device_id
):
    # Check that the device doesn't already exist
    client = iot_v1.DeviceManagerClient()

    exists = False

    parent = client.registry_path(project_id, cloud_region, registry_id)

    devices = list(client.list_devices(request={"parent": parent}))

    for device in devices:
        if device.id == device_id:
            exists = True

    # Create the device
    device_template = {
        "id": device_id,
        "gateway_config": {
            "gateway_type": iot_v1.GatewayType.NON_GATEWAY,
            "gateway_auth_method": iot_v1.GatewayAuthMethod.ASSOCIATION_ONLY,
        },
    }

    if not exists:
        res = client.create_device(
            request={"parent": parent, "device": device_template}
        )
        print("Created Device {}".format(res))
    else:
        print("Device exists, skipping")


def create_unauth_device(
    service_account_json, project_id, cloud_region, registry_id, device_id
):
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    device_template = {
        "id": device_id,
    }

    return client.create_device(request={"parent": parent, "device": device_template})


def delete_device(
    service_account_json, project_id, cloud_region, registry_id, device_id
):
    print("Delete device")
    client = iot_v1.DeviceManagerClient()

    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    return client.delete_device(request={"name": device_path})


def delete_registry(service_account_json, project_id, cloud_region, registry_id):
    print("Delete registry")

    client = iot_v1.DeviceManagerClient()
    registry_path = "projects/{}/locations/{}/registries/{}".format(
        project_id, cloud_region, registry_id
    )

    try:
        client.delete_device_registry(request={"name": registry_path})
        print("Deleted registry")
        return "Registry deleted"
    except HttpError:
        print("Error, registry not deleted")
        raise


def get_device(service_account_json, project_id, cloud_region, registry_id, device_id):
    print("Getting device")
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    device = client.get_device(request={"name": device_path})

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
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    device = client.get_device(request={"name": device_path})
    print("Last state: {}".format(device.state))

    print("State history")
    states = client.list_device_states(request={"name": device_path}).device_states

    # Avoid ReferenceError in py-3.9 builds.
    if states:
        for state in states:
            print("State: {}".format(state))

    return states


def list_devices(service_account_json, project_id, cloud_region, registry_id):
    print("Listing devices")

    client = iot_v1.DeviceManagerClient()
    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    devices = list(client.list_devices(request={"parent": registry_path}))
    for device in devices:
        print("Device: {} : {}".format(device.num_id, device.id))

    return devices


def list_registries(service_account_json, project_id, cloud_region):
    print("Listing Registries")
    client = iot_v1.DeviceManagerClient()
    parent = f"projects/{project_id}/locations/{cloud_region}"

    registries = list(client.list_device_registries(request={"parent": parent}))
    for registry in registries:
        print("id: {}\n\tname: {}".format(registry.id, registry.name))

    return registries


def create_registry(
    service_account_json, project_id, cloud_region, pubsub_topic, registry_id
):
    client = iot_v1.DeviceManagerClient()
    parent = f"projects/{project_id}/locations/{cloud_region}"

    if not pubsub_topic.startswith("projects/"):
        pubsub_topic = "projects/{}/topics/{}".format(project_id, pubsub_topic)

    body = {
        "event_notification_configs": [{"pubsub_topic_name": pubsub_topic}],
        "id": registry_id,
    }

    try:
        response = client.create_device_registry(
            request={"parent": parent, "device_registry": body}
        )
        print("Created registry")
        return response
    except HttpError:
        print("Error, registry not created")
        raise
    except AlreadyExists:
        print("Error, registry already exists")
        raise


def get_registry(service_account_json, project_id, cloud_region, registry_id):
    client = iot_v1.DeviceManagerClient()
    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    return client.get_device_registry(request={"name": registry_path})


def open_registry(
    service_account_json, project_id, cloud_region, pubsub_topic, registry_id
):
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
    print("Patch device with ES256 certificate")

    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    public_key_bytes = ""
    with io.open(public_key_file) as f:
        public_key_bytes = f.read()

    key = iot_v1.PublicKeyCredential(
        format=iot_v1.PublicKeyFormat.ES256_PEM, key=public_key_bytes
    )

    cred = iot_v1.DeviceCredential(public_key=key)
    device = client.get_device(request={"name": device_path})

    device.id = b""
    device.num_id = 0
    device.credentials.append(cred)

    mask = gp_field_mask.FieldMask()
    mask.paths.append("credentials")

    return client.update_device(request={"device": device, "update_mask": mask})


def patch_rsa256_auth(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    public_key_file,
):
    print("Patch device with RSA256 certificate")

    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    public_key_bytes = ""
    with io.open(public_key_file) as f:
        public_key_bytes = f.read()

    key = iot_v1.PublicKeyCredential(
        format=iot_v1.PublicKeyFormat.RSA_X509_PEM, key=public_key_bytes
    )

    cred = iot_v1.DeviceCredential(public_key=key)
    device = client.get_device(request={"name": device_path})

    device.id = b""
    device.num_id = 0
    device.credentials.append(cred)

    mask = gp_field_mask.FieldMask()
    mask.paths.append("credentials")

    return client.update_device(request={"device": device, "update_mask": mask})


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

    return client.modify_cloud_to_device_config(
        request={"name": device_path, "binary_data": data, "version_to_update": version}
    )


def get_config_versions(
    service_account_json, project_id, cloud_region, registry_id, device_id
):
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    configs = client.list_device_config_versions(request={"name": device_path})

    for config in configs.device_configs:
        print(
            "version: {}\n\tcloudUpdateTime: {}\n\t data: {}".format(
                config.version, config.cloud_update_time, config.binary_data
            )
        )

    return configs


def get_iam_permissions(service_account_json, project_id, cloud_region, registry_id):
    client = iot_v1.DeviceManagerClient()

    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    policy = client.get_iam_policy(request={"resource": registry_path})

    return policy


def set_iam_permissions(
    service_account_json, project_id, cloud_region, registry_id, role, member
):
    client = iot_v1.DeviceManagerClient()
    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    body = {"bindings": [{"members": [member], "role": role}]}

    return client.set_iam_policy(request={"resource": registry_path, "policy": body})


def send_command(
    service_account_json, project_id, cloud_region, registry_id, device_id, command
):
    print("Sending command to device")
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    # command = 'Hello IoT Core!'
    data = command.encode("utf-8")

    return client.send_command_to_device(
        request={"name": device_path, "binary_data": data}
    )


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
    exists = False
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)
    devices = list(client.list_devices(request={"parent": parent}))

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
        certificate_format = iot_v1.PublicKeyFormat.ES256_PEM
    else:
        certificate_format = iot_v1.PublicKeyFormat.RSA_X509_PEM

    device_template = {
        "id": gateway_id,
        "credentials": [
            {"public_key": {"format": certificate_format, "key": certificate}}
        ],
        "gateway_config": {
            "gateway_type": iot_v1.GatewayType.GATEWAY,
            "gateway_auth_method": iot_v1.GatewayAuthMethod.ASSOCIATION_ONLY,
        },
    }

    if not exists:
        res = client.create_device(
            request={"parent": parent, "device": device_template}
        )
        print("Created Gateway {}".format(res))
    else:
        print("Gateway exists, skipping")


def bind_device_to_gateway(
    service_account_json, project_id, cloud_region, registry_id, device_id, gateway_id
):
    client = iot_v1.DeviceManagerClient()

    create_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    parent = client.registry_path(project_id, cloud_region, registry_id)

    res = client.bind_device_to_gateway(
        request={"parent": parent, "gateway_id": gateway_id, "device_id": device_id}
    )

    print("Device Bound! {}".format(res))


def unbind_device_from_gateway(
    service_account_json, project_id, cloud_region, registry_id, device_id, gateway_id
):
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    res = client.unbind_device_from_gateway(
        request={"parent": parent, "gateway_id": gateway_id, "device_id": device_id}
    )

    print("Device unbound: {}".format(res))


def list_gateways(service_account_json, project_id, cloud_region, registry_id):
    client = iot_v1.DeviceManagerClient()

    path = client.registry_path(project_id, cloud_region, registry_id)
    mask = gp_field_mask.FieldMask()
    mask.paths.append("config")
    mask.paths.append("gateway_config")
    devices = list(client.list_devices(request={"parent": path, "field_mask": mask}))

    for device in devices:
        if device.gateway_config is not None:
            if device.gateway_config.gateway_type == 1:
                print("Gateway ID: {}\n\t{}".format(device.id, device))


def list_devices_for_gateway(
    service_account_json, project_id, cloud_region, registry_id, gateway_id
):
    client = iot_v1.DeviceManagerClient()

    path = client.registry_path(project_id, cloud_region, registry_id)

    devices = list(
        client.list_devices(
            request={
                "parent": path,
                "gateway_list_options": {"associations_gateway_id": gateway_id},
            }
        )
    )

    found = False
    for device in devices:
        found = True
        print("Device: {} : {}".format(device.num_id, device.id))

    if not found:
        print("No devices bound to gateway {}".format(gateway_id))
