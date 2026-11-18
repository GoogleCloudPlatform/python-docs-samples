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

# [START spanner_update_instance_default_backup_schedule_type]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def update_instance_default_backup_schedule_type(
    project_id: str, instance_id: str
) -> None:
    """Updates an instance to enable AUTOMATIC default backup schedules.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID to update.
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    instance_path = client.instance_path(project_id, instance_id)
    schedule_auto = (
        spanner_admin_instance_v1.Instance.DefaultBackupScheduleType.AUTOMATIC
    )
    instance_pb = spanner_admin_instance_v1.Instance(
        name=instance_path,
        default_backup_schedule_type=schedule_auto,
    )
    request = spanner_admin_instance_v1.UpdateInstanceRequest(
        instance=instance_pb,
        field_mask={"paths": ["default_backup_schedule_type"]},
    )

    try:
        operation = client.update_instance(request=request)
        print(
            f"Waiting for default_backup_schedule_type update on " f"'{instance_id}'..."
        )
        updated = operation.result(timeout=300)
    except exceptions.NotFound as err:
        print(
            f"error: instance '{instance_id}' was not found: {err.message}",
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
            f"error: failed to update default_backup_schedule_type on "
            f"instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        sched_type = updated.default_backup_schedule_type.name
        print(f"Resource ID: {instance_id}")
        print(f"Default Backup Schedule Type: {sched_type}")


# [END spanner_update_instance_default_backup_schedule_type]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Enable AUTOMATIC default backup schedules on a Spanner instance."
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

    update_instance_default_backup_schedule_type(
        project_id=args.project_id, instance_id=args.instance_id
    )
