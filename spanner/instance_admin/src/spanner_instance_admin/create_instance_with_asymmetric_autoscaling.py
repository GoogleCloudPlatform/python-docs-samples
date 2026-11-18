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

# [START spanner_create_instance_with_asymmetric_autoscaling]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def create_instance_with_asymmetric_autoscaling(
    project_id: str, instance_id: str
) -> None:
    """Creates a multi-region Spanner instance with asymmetric autoscaling.

    Asymmetric autoscaling lets a read-only replica region scale independently
    from the base multi-region autoscaling limits to serve localized read traffic.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The permanent ID for the new Spanner instance.
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    parent = f"projects/{project_id}"
    config_name = f"{parent}/instanceConfigs/nam9"
    instance_name = f"{parent}/instances/{instance_id}"

    base_limits = spanner_admin_instance_v1.AutoscalingConfig.AutoscalingLimits(
        min_nodes=1,
        max_nodes=2,
    )
    base_targets = spanner_admin_instance_v1.AutoscalingConfig.AutoscalingTargets(
        high_priority_cpu_utilization_percent=65,
        total_cpu_utilization_percent=80,
        storage_utilization_percent=95,
    )
    read_only_limits = spanner_admin_instance_v1.AutoscalingConfig.AutoscalingLimits(
        min_nodes=2,
        max_nodes=3,
    )
    overrides = spanner_admin_instance_v1.AutoscalingConfig.AsymmetricAutoscalingOption.AutoscalingConfigOverrides(
        autoscaling_limits=read_only_limits,
    )
    asymmetric_option = (
        spanner_admin_instance_v1.AutoscalingConfig.AsymmetricAutoscalingOption(
            replica_selection=spanner_admin_instance_v1.ReplicaSelection(
                location="us-west1"
            ),
            overrides=overrides,
        )
    )
    autoscaling_config = spanner_admin_instance_v1.AutoscalingConfig(
        autoscaling_limits=base_limits,
        autoscaling_targets=base_targets,
        asymmetric_autoscaling_options=[asymmetric_option],
    )
    instance = spanner_admin_instance_v1.Instance(
        name=instance_name,
        config=config_name,
        display_name="Asymmetric Autoscaling",
        edition=spanner_admin_instance_v1.Instance.Edition.ENTERPRISE_PLUS,
        autoscaling_config=autoscaling_config,
    )
    request = spanner_admin_instance_v1.CreateInstanceRequest(
        parent=parent,
        instance_id=instance_id,
        instance=instance,
    )

    try:
        operation = client.create_instance(request=request)
        print(f"Waiting for instance '{instance_id}' creation to complete...")
        created = operation.result(timeout=600)
    except exceptions.AlreadyExists as err:
        print(
            f"error: Spanner instance '{instance_id}' already exists: "
            f"{err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create asymmetric-autoscaling instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        asymmetric_options = (
            created.autoscaling_config.asymmetric_autoscaling_options
            if created.autoscaling_config
            else []
        )
        print(f"Resource ID: {instance_id}")
        print(f"Display Name: {created.display_name}")
        print(f"Asymmetric Overrides: {len(asymmetric_options)}")
        print(f"Instance State: {created.state.name}")


# [END spanner_create_instance_with_asymmetric_autoscaling]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a Spanner instance with asymmetric autoscaling."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Google Cloud project ID (default: $GOOGLE_CLOUD_PROJECT)",
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-asym-instance"),
        help="Spanner instance ID to create (default: $SPANNER_INSTANCE_ID)",
    )
    args = parser.parse_args()

    create_instance_with_asymmetric_autoscaling(
        project_id=args.project_id,
        instance_id=args.instance_id,
    )
