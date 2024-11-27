#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa

from google.cloud import compute_v1

# <INGREDIENT create_hyperdisk_storage_pool>


def create_hyperdisk_storage_pool(
    project_id: str,
    zone: str,
    storage_pool_name: str,
    storage_pool_type: str = "hyperdisk-balanced",
) -> compute_v1.StoragePool:
    """Creates a hyperdisk storage pool in the specified project and zone.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone where the storage pool will be created.
        storage_pool_name (str): The name of the storage pool.
        storage_pool_type (str, optional): The type of the storage pool. Defaults to "hyperdisk-balanced".
    Returns:
        compute_v1.StoragePool: The created storage pool.
    """

    pool = compute_v1.StoragePool()
    pool.name = storage_pool_name
    pool.zone = zone
    pool.storage_pool_type = (
        f"projects/{project_id}/zones/{zone}/storagePoolTypes/{storage_pool_type}"
    )
    pool.capacity_provisioning_type = "ADVANCED"
    pool.pool_provisioned_capacity_gb = 10240
    pool.performance_provisioning_type = "STANDARD"

    # Relevant if the storage pool type is hyperdisk-balanced.
    pool.pool_provisioned_iops = 10000
    pool.pool_provisioned_throughput = 1024

    pool_client = compute_v1.StoragePoolsClient()
    operation = pool_client.insert(
        project=project_id, zone=zone, storage_pool_resource=pool
    )
    wait_for_extended_operation(operation, "disk creation")

    new_pool = pool_client.get(project=project_id, zone=zone, storage_pool=pool.name)
    print(new_pool.pool_provisioned_iops)
    print(new_pool.pool_provisioned_throughput)
    print(new_pool.capacity_provisioning_type)
    # Example response:
    # 10000
    # 1024
    # ADVANCED

    return new_pool


# </INGREDIENT>
