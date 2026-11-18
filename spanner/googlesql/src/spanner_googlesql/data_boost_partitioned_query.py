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

# [START spanner_data_boost_partitioned_query]
import sys

from google.api_core import exceptions
from google.cloud import spanner


def run_data_boost_partitioned_query(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Executes a root-partitionable SQL query using Spanner Data Boost.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing the Singers table.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    sql = "SELECT SingerId, FirstName, LastName FROM Singers"

    # Data Boost runs partitioned queries on independent serverless compute
    # with near-zero impact on provisioned OLTP capacity.
    snapshot = database.batch_snapshot()
    total_rows = 0
    partition_count = 0

    try:
        partitions = snapshot.generate_query_batches(
            sql=sql,
            data_boost_enabled=True,
        )
        for partition in partitions:
            partition_count += 1
            for _row in snapshot.process_query_batch(partition):
                total_rows += 1
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: Data Boost partitioned query failed on database "
            f"'{database_id}' in instance '{instance_id}'"
            f": {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Partition Count: {partition_count}")
        print(f"Total Rows: {total_rows}")
    finally:
        snapshot.close()


# [END spanner_data_boost_partitioned_query]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Execute a partitioned SQL query using Spanner Data Boost."
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

    run_data_boost_partitioned_query(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
