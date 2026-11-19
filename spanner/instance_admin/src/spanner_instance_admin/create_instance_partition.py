# Copyright 2026 Google LLC
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

# [START spanner_create_instance_partition]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def create_instance_partition(
    project_id: str, instance_id: str, instance_partition_id: str
) -> None:
    """Creates a geo-partitioning InstancePartition on an Enterprise Plus instance.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Enterprise Plus Spanner instance ID.
        instance_partition_id: The new instance partition ID to create.
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    parent = client.instance_path(project_id, instance_id)
    config_path = client.instance_config_path(project_id, "nam6")
    partition_pb = spanner_admin_instance_v1.InstancePartition(
        config=config_path,
        display_name="Example Geo Partition",
        node_count=1,
    )
    request = spanner_admin_instance_v1.CreateInstancePartitionRequest(
        parent=parent,
        instance_partition_id=instance_partition_id,
        instance_partition=partition_pb,
    )

    try:
        operation = client.create_instance_partition(request=request)
        print(
            f"Waiting for instance partition '{instance_partition_id}' " f"creation..."
        )
        created = operation.result(timeout=300)
    except exceptions.AlreadyExists as err:
        print(
            f"error: instance partition '{instance_partition_id}' already "
            f"exists on instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except TimeoutError as err:
        print(
            f"error: timed out waiting for the operation on "
            f"instance partition '{instance_partition_id}' "
            f"to complete; the operation may still be running: {err}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create instance partition "
            f"'{instance_partition_id}' on instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {instance_partition_id}")
        print(f"Display Name: {created.display_name}")
        print(f"Partition State: {created.state.name}")


# [END spanner_create_instance_partition]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a geo-partitioning Spanner InstancePartition."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_MR_INSTANCE_ID", "example-ep-instance"),
    )
    parser.add_argument(
        "--instance-partition-id",
        default="example-partition",
    )
    args = parser.parse_args()

    create_instance_partition(
        project_id=args.project_id,
        instance_id=args.instance_id,
        instance_partition_id=args.instance_partition_id,
    )
