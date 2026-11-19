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

# [START spanner_delete_instance_config]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def delete_instance_config(project_id: str, custom_config_id: str) -> None:
    """Deletes an unused user-managed Spanner instance configuration.

    Args:
        project_id: The Google Cloud project ID.
        custom_config_id: The custom instance configuration ID to delete.
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    config_path = client.instance_config_path(project_id, custom_config_id)

    try:
        client.delete_instance_config(name=config_path)
    except exceptions.NotFound as err:
        print(
            f"error: custom instance config '{custom_config_id}' was not "
            f"found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to delete custom instance config "
            f"'{custom_config_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {custom_config_id}")
        print(f"Deleted Config: {custom_config_id}")


# [END spanner_delete_instance_config]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Delete a user-managed Spanner instance configuration."
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

    delete_instance_config(
        project_id=args.project_id, custom_config_id=args.custom_config_id
    )
