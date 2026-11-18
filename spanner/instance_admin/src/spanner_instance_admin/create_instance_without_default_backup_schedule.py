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

# [START spanner_create_instance_without_default_backup_schedule]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def create_instance_without_default_backup_schedule(
    project_id: str, instance_id: str
) -> None:
    """Creates a Spanner instance with DefaultBackupScheduleType.NONE.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The new Spanner instance ID to create.
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    parent = f"projects/{project_id}"
    config_path = client.instance_config_path(project_id, "regional-us-central1")
    schedule_none = spanner_admin_instance_v1.Instance.DefaultBackupScheduleType.NONE
    instance_pb = spanner_admin_instance_v1.Instance(
        config=config_path,
        display_name="No Default Schedule Instance",
        processing_units=100,
        default_backup_schedule_type=schedule_none,
    )
    request = spanner_admin_instance_v1.CreateInstanceRequest(
        parent=parent,
        instance_id=instance_id,
        instance=instance_pb,
    )

    try:
        operation = client.create_instance(request=request)
        print(f"Waiting for instance '{instance_id}' creation without schedules...")
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
            f"error: failed to create instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        sched_type = created.default_backup_schedule_type.name
        print(f"Resource ID: {instance_id}")
        print(f"Default Backup Schedule Type: {sched_type}")


# [END spanner_create_instance_without_default_backup_schedule]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a Spanner instance opting out of automatic backup schedules."
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

    create_instance_without_default_backup_schedule(
        project_id=args.project_id, instance_id=args.instance_id
    )
