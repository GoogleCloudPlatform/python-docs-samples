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

# [START spanner_create_instance_with_autoscaling_config]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def create_instance_with_autoscaling_config(project_id: str, instance_id: str) -> None:
    """Creates an Enterprise Spanner instance with managed autoscaling limits.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The new Spanner instance ID to create.
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    parent = f"projects/{project_id}"
    config_path = client.instance_config_path(project_id, "regional-us-central1")
    limits = spanner_admin_instance_v1.AutoscalingConfig.AutoscalingLimits(
        min_nodes=1,
        max_nodes=2,
    )
    targets = spanner_admin_instance_v1.AutoscalingConfig.AutoscalingTargets(
        high_priority_cpu_utilization_percent=65,
        storage_utilization_percent=95,
    )
    autoscaling_config = spanner_admin_instance_v1.AutoscalingConfig(
        autoscaling_limits=limits,
        autoscaling_targets=targets,
    )
    instance_pb = spanner_admin_instance_v1.Instance(
        config=config_path,
        display_name="Autoscaling Example Instance",
        autoscaling_config=autoscaling_config,
        labels={"cloud_spanner_samples": "true"},
        edition=spanner_admin_instance_v1.Instance.Edition.ENTERPRISE,
    )
    request = spanner_admin_instance_v1.CreateInstanceRequest(
        parent=parent,
        instance_id=instance_id,
        instance=instance_pb,
    )

    try:
        operation = client.create_instance(request=request)
        print(f"Waiting for autoscaling instance '{instance_id}' creation...")
        created = operation.result(timeout=300)
    except exceptions.AlreadyExists as err:
        print(
            f"error: instance '{instance_id}' already exists: {err.message}",
            file=sys.stderr,
        )
    except TimeoutError as err:
        print(
            f"error: timed out waiting for the operation on instance '{instance_id}' "
            f"to complete; the operation may still be running: {err}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create autoscaling instance '{instance_id}': "
            f"{err.message}",
            file=sys.stderr,
        )
    else:
        max_nodes = created.autoscaling_config.autoscaling_limits.max_nodes
        min_nodes = created.autoscaling_config.autoscaling_limits.min_nodes
        print(f"Resource ID: {instance_id}")
        print(f"Max Nodes: {max_nodes}")
        print(f"Min Nodes: {min_nodes}")


# [END spanner_create_instance_with_autoscaling_config]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create an Enterprise Spanner instance with managed autoscaling."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
    )
    args = parser.parse_args()

    create_instance_with_autoscaling_config(
        project_id=args.project_id, instance_id=args.instance_id
    )
