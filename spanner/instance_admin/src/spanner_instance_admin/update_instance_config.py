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

# [START spanner_update_instance_config]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def update_instance_config(project_id: str, custom_config_id: str) -> None:
    """Updates display_name and labels on a custom Spanner instance config.

    Args:
        project_id: The Google Cloud project ID.
        custom_config_id: The user-managed instance configuration ID.
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    config_path = client.instance_config_path(project_id, custom_config_id)

    try:
        config = client.get_instance_config(name=config_path)
        config.display_name = "Updated Custom Instance Config"
        config.labels["updated"] = "true"
        request = spanner_admin_instance_v1.UpdateInstanceConfigRequest(
            instance_config=config,
            update_mask={"paths": ["display_name", "labels"]},
        )
        operation = client.update_instance_config(request=request)
        print(f"Waiting for custom instance config '{custom_config_id}' update...")
        updated = operation.result(timeout=300)
    except exceptions.NotFound as err:
        print(
            f"error: custom instance config '{custom_config_id}' was not "
            f"found: {err.message}",
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
            f"error: failed to update custom instance config "
            f"'{custom_config_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {custom_config_id}")
        print(f"Display Name: {updated.display_name}")
        print(f"Label Count: {len(updated.labels)}")


# [END spanner_update_instance_config]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Update display_name and labels on a custom instance config."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--custom-config-id",
        default="custom-example-nam11",
    )
    args = parser.parse_args()

    update_instance_config(
        project_id=args.project_id, custom_config_id=args.custom_config_id
    )
