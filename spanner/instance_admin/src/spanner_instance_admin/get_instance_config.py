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

# [START spanner_get_instance_config]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def get_instance_config(project_id: str, instance_config_id: str) -> None:
    """Retrieves metadata and leader options for a Spanner instance config.

    Args:
        project_id: The Google Cloud project ID.
        instance_config_id: The Spanner instance configuration ID (for example, 'nam3').
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    config_path = client.instance_config_path(project_id, instance_config_id)

    try:
        config = client.get_instance_config(name=config_path)
    except exceptions.NotFound as err:
        print(
            f"error: instance config '{instance_config_id}' was not found: "
            f"{err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to get instance config '{instance_config_id}': "
            f"{err.message}",
            file=sys.stderr,
        )
    else:
        leaders = list(config.leader_options)
        print(f"Resource ID: {instance_config_id}")
        print(f"Display Name: {config.display_name}")
        print(f"Leader Options: {leaders}")
        print(f"Replica Count: {len(config.replicas)}")


# [END spanner_get_instance_config]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Get metadata and leader options for a Spanner instance config."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--instance-config-id",
        default="nam3",
    )
    args = parser.parse_args()

    get_instance_config(
        project_id=args.project_id,
        instance_config_id=args.instance_config_id,
    )
