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

# [START spanner_field_access_on_nested_struct_parameters]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def query_nested_struct_field(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Queries Singers accessing nested ARRAY<STRUCT> fields on a STRUCT parameter.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing the Singers table.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    artist_type = param_types.Struct(
        [
            param_types.StructField("FirstName", param_types.STRING),
            param_types.StructField("LastName", param_types.STRING),
        ]
    )
    song_info_type = param_types.Struct(
        [
            param_types.StructField("SongName", param_types.STRING),
            param_types.StructField("ArtistNames", param_types.Array(artist_type)),
        ]
    )
    artists = [("Elena", "Campbell"), ("Hannah", "Harris")]
    song_info = ("Imagination", artists)

    try:
        with database.snapshot() as snapshot:
            rows = list(
                snapshot.execute_sql(
                    """
                    SELECT SingerId, @song_info.SongName
                    FROM Singers WHERE
                    STRUCT<FirstName STRING, LastName STRING>
                    (FirstName, LastName)
                    IN UNNEST(@song_info.ArtistNames)
                    """,
                    params={"song_info": song_info},
                    param_types={"song_info": song_info_type},
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
            f"error: nested STRUCT field query failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Row Count: {len(rows)}")
        for singer_id, song_name in rows:
            print(f"Singer ID: {singer_id}, Song Name: {song_name}")


# [END spanner_field_access_on_nested_struct_parameters]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Query Singers accessing nested fields on a STRUCT parameter."
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

    query_nested_struct_field(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
