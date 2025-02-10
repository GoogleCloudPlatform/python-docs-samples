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
# flake8: noqa

from google.cloud import compute_v1


# <INGREDIENT stop_replication_in_consistency_group>
def stop_replication_consistency_group(project_id, location, consistency_group_name):
    """
    Stops the asynchronous replication for a consistency group.
    Args:
        project_id (str): The ID of the Google Cloud project.
        location (str): The region where the consistency group is located.
        consistency_group_id (str): The ID of the consistency group.
    Returns:
        bool: True if the replication was successfully stopped.
    """
    consistency_group = compute_v1.DisksStopGroupAsyncReplicationResource(
        resource_policy=f"regions/{location}/resourcePolicies/{consistency_group_name}"
    )
    region_client = compute_v1.RegionDisksClient()
    operation = region_client.stop_group_async_replication(
        project=project_id,
        region=location,
        disks_stop_group_async_replication_resource_resource=consistency_group,
    )
    wait_for_extended_operation(operation, "Stopping replication for consistency group")

    return True


# </INGREDIENT>
