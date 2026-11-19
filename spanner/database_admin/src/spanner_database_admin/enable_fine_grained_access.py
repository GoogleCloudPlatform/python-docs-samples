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

# [START spanner_enable_fine_grained_access]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def enable_fine_grained_access(
    project_id: str,
    instance_id: str,
    database_id: str,
    iam_member: str,
    database_role: str,
) -> None:
    """Grants conditional fineGrainedAccessUser IAM access for a database role.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID.
        iam_member: The IAM principal (for example, 'user:alice@example.com').
        database_role: The target Spanner database role name.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    database_path = client.database_path(project_id, instance_id, database_id)
    get_request = {
        "resource": database_path,
        "options": {"requested_policy_version": 3},
    }
    condition_expr = f'resource.name.endsWith("/databaseRoles/{database_role}")'

    try:
        policy = client.get_iam_policy(request=get_request)
        policy.version = 3
        binding = policy.bindings.add(
            role="roles/spanner.fineGrainedAccessUser",
            members=[iam_member],
        )
        binding.condition.title = f"fgac_{database_role}"
        binding.condition.expression = condition_expr
        updated_policy = client.set_iam_policy(
            request={"resource": database_path, "policy": policy}
        )
    except exceptions.InvalidArgument as err:
        print(
            f"error: invalid IAM principal or conditional binding for role "
            f"'{database_role}' on database '{database_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to enable fine-grained access on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Database Role: {database_role}")
        print(f"Policy Version: {updated_policy.version}")


# [END spanner_enable_fine_grained_access]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Grant conditional IAM access to a Spanner database role."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
    )
    parser.add_argument(
        "--database-id",
        default=os.environ.get("SPANNER_DATABASE_ID", "example-db"),
    )
    parser.add_argument(
        "--iam-member",
        default=os.environ.get("SPANNER_FGAC_IAM_MEMBER", "user:alice@example.com"),
    )
    parser.add_argument(
        "--database-role",
        default="new_parent",
    )
    args = parser.parse_args()

    enable_fine_grained_access(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
        iam_member=args.iam_member,
        database_role=args.database_role,
    )
