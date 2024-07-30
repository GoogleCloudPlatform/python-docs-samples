# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START memorystorememcache_quickstart]
import uuid

from google.api_core.exceptions import NotFound
from google.cloud import memcache_v1


def create_instance(project_id: str, location_id: str, instance_id: str) -> None:
    """
    Creates a Memcached instance.

    project_id: ID or number of the Google Cloud project you want to use.
    location_id: A GCP region, where instance is going to be located.
    instance_id: Unique id of the instance. Must be unique within the user project / location.
    """

    client = memcache_v1.CloudMemcacheClient()
    parent = f"projects/{project_id}/locations/{location_id}"

    instance = memcache_v1.Instance()
    instance.name = "memcache_instance_name"
    instance.node_count = 1
    instance.node_config.cpu_count = 1
    instance.node_config.memory_size_mb = 1024

    request = memcache_v1.CreateInstanceRequest(
        parent=parent,
        instance_id=instance_id,
        instance=instance,
    )

    print(f"Creating instance {instance_id}...")
    operation = client.create_instance(request=request)
    operation.result()
    print(f"Instance {instance_id} was created")


def get_instance(project_id: str, location_id: str, instance_id: str) -> memcache_v1.Instance:
    """
    Get a Memcached instance.

    project_id: ID or number of the Google Cloud project you want to use.
    location_id: A GCP region, where instance is located.
    instance_id: Unique id of the instance. Must be unique within the user project / location.
    """

    client = memcache_v1.CloudMemcacheClient()

    name = f"projects/{project_id}/locations/{location_id}/instances/{instance_id}"
    request = memcache_v1.GetInstanceRequest(
        name=name
    )

    try:
        instance = client.get_instance(request=request)
        return instance
    except NotFound:
        print("Instance wasn't found")


def update_instance(instance: memcache_v1.Instance, display_name: str) -> None:
    """
    Updates a Memcached instance.

    instance_id: Unique id of the instance. Must be unique within the user project / location.
    display_name: New name of the instance to be set.
    """

    client = memcache_v1.CloudMemcacheClient()

    instance.display_name = display_name
    request = memcache_v1.UpdateInstanceRequest(
        update_mask="displayName",
        instance=instance,
    )

    operation = client.update_instance(request=request)
    result = operation.result()
    print(f"New name is: {result.display_name}")


def delete_instance(project_id: str, location_id: str, instance_id: str) -> None:
    """
    Deletes a Memcached instance.

    project_id: ID or number of the Google Cloud project you want to use.
    location_id: A GCP region, where instance is located.
    instance_id: Unique id of the instance. Must be unique within the user project / location.
    """

    client = memcache_v1.CloudMemcacheClient()

    name = f"projects/{project_id}/locations/{location_id}/instances/{instance_id}"
    request = memcache_v1.DeleteInstanceRequest(
        name=name
    )

    try:
        operation = client.delete_instance(request=request)
        operation.result()
        print(f"Instance {instance_id} was deleted")
    except NotFound:
        print("Instance wasn't found")


def quickstart(project_id: str, location_id: str, instance_id: str) -> None:
    """
    Briefly demonstrates a full lifecycle of the Memcached instances.

    project_id: ID or number of the Google Cloud project you want to use.
    location_id: A GCP region, where instance is located.
    instance_id: Unique id of the instance. Must be unique within the user project / location.
    """

    create_instance(project_id, location_id, instance_id)
    instance = get_instance(project_id, location_id, instance_id)
    update_instance(instance, "new_name")
    delete_instance(project_id, location_id, instance_id)

# [END memorystorememcache_quickstart]


if __name__ == "__main__":
    # Note: To run the sample private connection should be enabled
    # https://cloud.google.com/vpc/docs/configure-private-services-access
    #
    # Permissions needed:
    # - Compute Network Admin (servicenetworking.services.addPeering)
    # - Cloud Memorystore Memcached Admin (memcache.*)
    import google.auth

    PROJECT = google.auth.default()[1]
    instance_id = f"memcache-{uuid.uuid4().hex[:10]}"
    location_id = "us-central1"

    quickstart(PROJECT, location_id, instance_id)
