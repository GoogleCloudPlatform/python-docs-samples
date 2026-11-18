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

# [START spanner_set_transaction_tag]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1
from google.cloud.spanner_v1 import param_types


def set_transaction_tag(project_id: str, instance_id: str, database_id: str) -> None:
    """Sets a transaction_tag and per-statement request_tags in a transaction.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Venues.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    update_opts = spanner_v1.RequestOptions(
        request_tag="app=concert,env=dev,action=update"
    )
    insert_opts = spanner_v1.RequestOptions(
        request_tag="app=concert,env=dev,action=insert"
    )
    venue_params = {
        "venueId": 81,
        "venueName": "Venue 81",
        "capacity": 1440,
        "outdoorVenue": True,
    }
    venue_types = {
        "venueId": param_types.INT64,
        "venueName": param_types.STRING,
        "capacity": param_types.INT64,
        "outdoorVenue": param_types.BOOL,
    }
    updated_rows = 0
    inserted_rows = 0

    def update_venues(transaction: spanner_v1.transaction.Transaction) -> None:
        nonlocal updated_rows, inserted_rows
        updated_rows = transaction.execute_update(
            "UPDATE Venues SET Capacity = DIV(Capacity, 4) "
            "WHERE OutdoorVenue = false AND VenueId IN (4, 42)",
            request_options=update_opts,
        )
        inserted_rows = transaction.execute_update(
            "INSERT INTO Venues "
            "(VenueId, VenueName, Capacity, OutdoorVenue, LastUpdateTime) "
            "VALUES (@venueId, @venueName, @capacity, @outdoorVenue, "
            "PENDING_COMMIT_TIMESTAMP())",
            params=venue_params,
            param_types=venue_types,
            request_options=insert_opts,
        )

    try:
        database.run_in_transaction(
            update_venues, transaction_tag="app=concert,env=dev"
        )
    except exceptions.AlreadyExists as err:
        print(
            f"error: venue row already exists on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: tagged transaction failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Inserted Rows: {inserted_rows}")
        print(f"Updated Rows: {updated_rows}")


# [END spanner_set_transaction_tag]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Attach transaction_tag and request_tag labels to a DML transaction."
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

    set_transaction_tag(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
