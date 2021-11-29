#!/usr/bin/env python

# Copyright 2021 Google LLC
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
A sample script showing how to start and stop Google Compute Engine instances.
"""

# [START compute_start_instance]
# [START compute_start_enc_instance]
# [START compute_stop_instance]
# [START compute_reset_instance]
from google.cloud import compute_v1

# [END compute_reset_instance]
# [END compute_stop_instance]
# [END compute_start_enc_instance]
# [END compute_start_instance]


# [START compute_start_instance]
def start_instance(project_id: str, zone: str, instance_name: str):
    """
    Starts a stopped Google Compute Engine instance (with unencrypted disks).

    Args:
        project_id: project ID or project number of the Cloud project your instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance your want to start.
    """
    instance_client = compute_v1.InstancesClient()
    op_client = compute_v1.ZoneOperationsClient()

    op = instance_client.start(project=project_id, zone=zone, instance=instance_name)

    while op.status != compute_v1.Operation.Status.DONE:
        op = op_client.wait(operation=op.name, zone=zone, project=project_id)
    return


# [END compute_start_instance]


# [START compute_start_enc_instance]
def start_instance_with_encryption_key(
    project_id: str, zone: str, instance_name: str, key: bytes
):
    """
    Starts a stopped Google Compute Engine instance (with encrypted disks).

    Args:
        project_id: project ID or project number of the Cloud project your instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance your want to start.
        key: bytes object representing a raw base64 encoded key to your machines boot disk.
            For more information about disk encryption see:
            https://cloud.google.com/compute/docs/disks/customer-supplied-encryption#specifications
    """
    instance_client = compute_v1.InstancesClient()
    op_client = compute_v1.ZoneOperationsClient()

    instance_data = instance_client.get(
        project=project_id, zone=zone, instance=instance_name
    )

    # Prepare the information about disk encryption
    disk_data = compute_v1.CustomerEncryptionKeyProtectedDisk()
    disk_data.source = instance_data.disks[0].source
    disk_data.disk_encryption_key = compute_v1.CustomerEncryptionKey()
    # Use raw_key to send over the key to unlock the disk
    # To use a key stored in KMS, you need to provide `kms_key_name` and `kms_key_service_account`
    disk_data.disk_encryption_key.raw_key = key
    enc_data = compute_v1.InstancesStartWithEncryptionKeyRequest()
    enc_data.disks = [disk_data]

    op = instance_client.start_with_encryption_key(
        project=project_id,
        zone=zone,
        instance=instance_name,
        instances_start_with_encryption_key_request_resource=enc_data,
    )

    while op.status != compute_v1.Operation.Status.DONE:
        op = op_client.wait(operation=op.name, zone=zone, project=project_id)
    return


# [END compute_start_enc_instance]


# [START compute_stop_instance]
def stop_instance(project_id: str, zone: str, instance_name: str):
    """
    Stops a stopped Google Compute Engine instance.

    Args:
        project_id: project ID or project number of the Cloud project your instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance your want to stop.
    """
    instance_client = compute_v1.InstancesClient()
    op_client = compute_v1.ZoneOperationsClient()

    op = instance_client.stop(project=project_id, zone=zone, instance=instance_name)

    while op.status != compute_v1.Operation.Status.DONE:
        op = op_client.wait(operation=op.name, zone=zone, project=project_id)
    return


# [END compute_stop_instance]


# [START compute_reset_instance]
def reset_instance(project_id: str, zone: str, instance_name: str):
    """
    Resets a stopped Google Compute Engine instance (with unencrypted disks).

    Args:
        project_id: project ID or project number of the Cloud project your instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance your want to reset.
    """
    instance_client = compute_v1.InstancesClient()
    op_client = compute_v1.ZoneOperationsClient()

    op = instance_client.reset(project=project_id, zone=zone, instance=instance_name)

    while op.status != compute_v1.Operation.Status.DONE:
        op = op_client.wait(operation=op.name, zone=zone, project=project_id)
    return


# [END compute_reset_instance]
