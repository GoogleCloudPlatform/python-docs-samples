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

# [START spanner_create_instance_config]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def create_instance_config(
    project_id: str, custom_config_id: str, base_config_id: str
) -> None:
    """Creates a custom Spanner instance config by adding an optional replica.

    Args:
        project_id: The Google Cloud project ID.
        custom_config_id: The new custom config ID (must start with 'custom-').
        base_config_id: The Google-managed base config ID (for example, 'nam11').
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    parent = f"projects/{project_id}"
    base_config_path = client.instance_config_path(project_id, base_config_id)
    custom_config_path = client.instance_config_path(project_id, custom_config_id)

    try:
        base_config = client.get_instance_config(name=base_config_path)
        if not base_config.optional_replicas:
            raise ValueError("base config has no optional replicas to add")
        replicas = list(base_config.replicas) + [base_config.optional_replicas[0]]
        custom_config = spanner_admin_instance_v1.InstanceConfig(
            name=custom_config_path,
            display_name="Custom Python Sample Config",
            config_type=spanner_admin_instance_v1.InstanceConfig.Type.USER_MANAGED,
            replicas=replicas,
            base_config=base_config.name,
            labels={"cloud_spanner_samples": "true"},
        )
        request = spanner_admin_instance_v1.CreateInstanceConfigRequest(
            parent=parent,
            instance_config_id=custom_config_id,
            instance_config=custom_config,
        )
        operation = client.create_instance_config(request=request)
        print(f"Waiting for custom instance config '{custom_config_id}'...")
        created = operation.result(timeout=300)
    except ValueError as err:
        print(
            f"error: cannot create custom instance config from base config "
            f"'{base_config_id}': {err}",
            file=sys.stderr,
        )
    except exceptions.AlreadyExists as err:
        print(
            f"error: custom instance config '{custom_config_id}' already "
            f"exists: {err.message}",
            file=sys.stderr,
        )
    except TimeoutError as err:
        print(
            f"error: timed out waiting for the operation on "
            f"custom config '{custom_config_id}' "
            f"to complete; the operation may still be running: {err}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create custom instance config "
            f"'{custom_config_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {custom_config_id}")
        print(f"Display Name: {created.display_name}")
        print(f"Replica Count: {len(created.replicas)}")


# [END spanner_create_instance_config]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a custom user-managed Spanner instance configuration."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--custom-config-id",
        default="custom-example-nam11",
    )
    parser.add_argument(
        "--base-config-id",
        default="nam11",
    )
    args = parser.parse_args()

    create_instance_config(
        project_id=args.project_id,
        custom_config_id=args.custom_config_id,
        base_config_id=args.base_config_id,
    )
