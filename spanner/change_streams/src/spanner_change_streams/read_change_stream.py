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

# [START spanner_read_change_stream]
from datetime import datetime, timedelta, timezone
import sys

from google.api_core import exceptions
from google.cloud import spanner_v1
from google.protobuf import struct_pb2


def read_change_stream(project_id: str, instance_id: str, database_id: str) -> None:
    """Streams initial partition records from a Spanner change stream TVF.

    Change stream TVF queries require a single-use strong read executed via the
    ExecuteStreamingSql RPC.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing SingersAndAlbumsStream.
    """
    client = spanner_v1.SpannerClient()
    database_name = (
        f"projects/{project_id}/instances/{instance_id}/databases/{database_id}"
    )
    now = datetime.now(timezone.utc)
    end_ts = (now - timedelta(seconds=2)).isoformat().replace("+00:00", "Z")
    start_ts = (now - timedelta(seconds=7)).isoformat().replace("+00:00", "Z")

    params = struct_pb2.Struct()
    params.update({"start_ts": start_ts, "end_ts": end_ts})
    ts_type = spanner_v1.Type(code=spanner_v1.TypeCode.TIMESTAMP)
    read_only = spanner_v1.TransactionOptions.ReadOnly(strong=True)
    selector = spanner_v1.TransactionSelector(
        single_use=spanner_v1.TransactionOptions(read_only=read_only)
    )
    sql = """
        SELECT ChangeRecord
        FROM READ_SingersAndAlbumsStream(
            start_timestamp => @start_ts,
            end_timestamp => @end_ts,
            partition_token => NULL,
            heartbeat_milliseconds => 10000
        )
    """

    try:
        # Multiplexed sessions are managed by Spanner and do not support DeleteSession.
        session_req = spanner_v1.CreateSessionRequest(
            database=database_name,
            session=spanner_v1.Session(multiplexed=True),
        )
        session = client.create_session(request=session_req)
        sql_req = spanner_v1.ExecuteSqlRequest(
            session=session.name,
            sql=sql,
            params=params,
            param_types={"start_ts": ts_type, "end_ts": ts_type},
            transaction=selector,
        )
        chunks = list(client.execute_streaming_sql(request=sql_req))
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: change stream read failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print("Change Stream: SingersAndAlbumsStream")
        print(f"Stream Chunks Received: {len(chunks)}")


# [END spanner_read_change_stream]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Read initial partition records from a Spanner change stream TVF."
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

    read_change_stream(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
