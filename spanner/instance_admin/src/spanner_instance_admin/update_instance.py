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

# [START spanner_update_instance]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_instance_v1


def update_instance(project_id: str, instance_id: str) -> None:
    """Updates labels and Enterprise edition on a Cloud Spanner instance.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID to update.
    """
    client = spanner_admin_instance_v1.InstanceAdminClient()
    instance_path = client.instance_path(project_id, instance_id)
    instance_pb = spanner_admin_instance_v1.Instance(
        name=instance_path,
        labels={"cloud_spanner_samples": "updated"},
        edition=spanner_admin_instance_v1.Instance.Edition.ENTERPRISE,
    )
    request = spanner_admin_instance_v1.UpdateInstanceRequest(
        instance=instance_pb,
        field_mask={"paths": ["labels", "edition"]},
    )

    try:
        operation = client.update_instance(request=request)
        print(f"Waiting for instance '{instance_id}' update to complete...")
        updated = operation.result(timeout=600)
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
            f"error: failed to update instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {instance_id}")
        print(f"Edition: {updated.edition.name}")
        print(f"Label Count: {len(updated.labels)}")


# [END spanner_update_instance]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Update labels and edition on a Spanner instance."
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

    update_instance(project_id=args.project_id, instance_id=args.instance_id)
