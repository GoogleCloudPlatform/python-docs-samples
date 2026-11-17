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

# [START spanner_opentelemetry_capture_query_stats_metric]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


def capture_query_stats_metric(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Records Spanner query-execution elapsed time into an OpenTelemetry histogram.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing the Singers table.
    """
    exporter = OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True)
    reader = PeriodicExportingMetricReader(exporter)
    meter_provider = MeterProvider(metric_readers=[reader])
    meter = meter_provider.get_meter("spanner-query-stats-sample")
    query_latency = meter.create_histogram(
        name="spanner/query_stats_elapsed",
        unit="ms",
        description="Spanner server-side SQL query execution latency.",
    )

    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    elapsed_ms = 0.0

    try:
        with database.snapshot() as snapshot:
            results = snapshot.execute_sql(
                "SELECT SingerId, FirstName FROM Singers LIMIT 5",
                query_mode=spanner_v1.ExecuteSqlRequest.QueryMode.PROFILE,
            )
            rows = list(results)
            raw_elapsed = str(results.stats.query_stats.get("elapsed_time", "0 msecs"))
            elapsed_ms = float(raw_elapsed.split()[0])
            query_latency.record(elapsed_ms, {"database": database_id})
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"in project '{project_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: profiled query failed on database '{database_id}' "
            f"in instance '{instance_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        print(f"Elapsed Milliseconds: {elapsed_ms:.2f}")
        print("Metric Name: spanner/query_stats_elapsed")
        print(f"Row Count: {len(rows)}")
    finally:
        meter_provider.shutdown()


# [END spanner_opentelemetry_capture_query_stats_metric]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Capture Spanner query execution latency with OpenTelemetry."
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

    capture_query_stats_metric(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
