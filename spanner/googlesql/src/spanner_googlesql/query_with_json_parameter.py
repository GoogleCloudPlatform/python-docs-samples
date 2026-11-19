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

# [START spanner_query_with_json_parameter]
import json
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def query_with_json_parameter(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Queries a GoogleSQL JSON column comparing JSON_VALUE against a bound JSON parameter.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID with Venues.VenueDetails JSON.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    details_json = json.dumps({"rating": 9})

    try:
        with database.snapshot() as snapshot:
            rows = list(
                snapshot.execute_sql(
                    """
                    SELECT VenueId, VenueDetails
                    FROM Venues
                    WHERE JSON_VALUE(VenueDetails, '$.rating') =
                    JSON_VALUE(@details, '$.rating')
                    """,
                    params={"details": details_json},
                    param_types={"details": param_types.JSON},
                )
            )
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: JSON parameter query failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Row Count: {len(rows)}")
        for venue_id, venue_details in rows:
            print(f"Venue ID: {venue_id}, Details: {venue_details}")


# [END spanner_query_with_json_parameter]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Query Venues.VenueDetails using a bound GoogleSQL JSON parameter."
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

    query_with_json_parameter(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
