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

# [START spanner_update_data_with_numeric_column]
import decimal
import sys

from google.api_core import exceptions
from google.cloud import spanner


def update_data_with_numeric(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Writes exact decimal.Decimal values into a GoogleSQL NUMERIC column.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID with Venues.Revenue NUMERIC.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    venue_updates = [
        (4, decimal.Decimal("35000")),
        (19, decimal.Decimal("104500")),
        (42, decimal.Decimal("99999999999999999999999999999.99")),
    ]

    try:
        with database.batch() as batch:
            batch.update(
                table="Venues",
                columns=("VenueId", "Revenue"),
                values=venue_updates,
            )
    except exceptions.NotFound as err:
        print(
            f"error: target venue row or database '{database_id}' on instance "
            f"'{instance_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: NUMERIC batch update failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Updated Venues: {len(venue_updates)}")


# [END spanner_update_data_with_numeric_column]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Update Venues.Revenue with exact decimal.Decimal values."
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

    update_data_with_numeric(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
