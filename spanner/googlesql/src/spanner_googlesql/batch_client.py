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

# [START spanner_batch_client]
from concurrent import futures
import sys
import threading

from google.api_core import exceptions
from google.cloud import spanner


def run_batch_read(project_id: str, instance_id: str, database_id: str) -> None:
    """Partitions a table read with Data Boost and processes batches concurrently.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing the Singers table.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    batch_snapshot = None
    partition_count = 0
    total_rows = 0
    row_lock = threading.Lock()

    def process_partition(partition: dict[str, object]) -> None:
        nonlocal total_rows
        assert batch_snapshot is not None
        count = sum(1 for _ in batch_snapshot.process_read_batch(partition))
        with row_lock:
            total_rows += count

    try:
        batch_snapshot = database.batch_snapshot()
        partitions = list(
            batch_snapshot.generate_read_batches(
                table="Singers",
                columns=("SingerId", "FirstName", "LastName"),
                keyset=spanner.KeySet(all_=True),
                data_boost_enabled=True,
            )
        )
        partition_count = len(partitions)
        with futures.ThreadPoolExecutor() as executor:
            list(executor.map(process_partition, partitions))
    except exceptions.NotFound as err:
        print(
            f"error: table or database '{database_id}' on instance "
            f"'{instance_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: partitioned batch read failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Partition Count: {partition_count}")
        print(f"Total Rows: {total_rows}")
    finally:
        if batch_snapshot is not None:
            batch_snapshot.close()


# [END spanner_batch_client]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Partition a Singers read across worker threads using BatchSnapshot."
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

    run_batch_read(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
