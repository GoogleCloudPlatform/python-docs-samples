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

# [START spanner_list_instance_configs]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def list_instance_configs(project_id: str) -> None:
    """Lists available Google-managed and custom Spanner instance configs.

    Args:
        project_id: The Google Cloud project ID.
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    request = spanner_admin_instance_v1.ListInstanceConfigsRequest(
        parent=f"projects/{project_id}"
    )

    try:
        configs = list(client.list_instance_configs(request=request))
    except exceptions.PermissionDenied as err:
        print(
            f"error: permission denied listing Spanner instance configs: "
            f"{err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to list Spanner instance configs: {err.message}",
            file=sys.stderr,
        )
    else:
        for cfg in configs[:5]:
            cfg_id = cfg.name.split("/")[-1]
            print(f"Resource ID: {cfg_id}")
            print(f"Leader Options: {list(cfg.leader_options)}")
        print(f"Total Instance Configs: {len(configs)}")


# [END spanner_list_instance_configs]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="List available Spanner instance configurations."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    args = parser.parse_args()

    list_instance_configs(project_id=args.project_id)
