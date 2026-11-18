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

# [START spanner_add_and_drop_database_role]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def add_and_drop_database_role(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Creates fine-grained database roles, grants privileges, and drops child role.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Singers.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    database_path = client.database_path(project_id, instance_id, database_id)
    role_parent = "new_parent"
    role_child = "new_child"
    create_request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
        database=database_path,
        statements=[
            f"CREATE ROLE {role_parent}",
            f"GRANT SELECT ON TABLE Singers TO ROLE {role_parent}",
            f"CREATE ROLE {role_child}",
            f"GRANT ROLE {role_parent} TO ROLE {role_child}",
        ],
    )
    drop_request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
        database=database_path,
        statements=[
            f"REVOKE ROLE {role_parent} FROM ROLE {role_child}",
            f"DROP ROLE {role_child}",
        ],
    )

    try:
        create_op = client.update_database_ddl(request=create_request)
        print(f"Waiting for database roles '{role_parent}' and '{role_child}'...")
        create_op.result(timeout=300)
        drop_op = client.update_database_ddl(request=drop_request)
        print(f"Waiting for child role '{role_child}' revocation and drop...")
        drop_op.result(timeout=300)
    except (exceptions.AlreadyExists, exceptions.FailedPrecondition) as err:
        print(
            f"error: database role already exists or preconditions failed on "
            f"database '{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except TimeoutError as err:
        print(
            f"error: timed out waiting for the operation on database '{database_id}' "
            f"to complete; the operation may still be running: {err}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to manage database roles on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Active Role: {role_parent}")
        print(f"Dropped Role: {role_child}")


# [END spanner_add_and_drop_database_role]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create, grant, revoke, and drop Spanner fine-grained database roles."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Google Cloud project ID (default: $GOOGLE_CLOUD_PROJECT)",
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
        help="Spanner instance ID (default: $SPANNER_INSTANCE_ID)",
    )
    parser.add_argument(
        "--database-id",
        default=os.environ.get("SPANNER_DATABASE_ID", "example-db"),
        help="Spanner database ID (default: $SPANNER_DATABASE_ID)",
    )
    args = parser.parse_args()

    add_and_drop_database_role(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
