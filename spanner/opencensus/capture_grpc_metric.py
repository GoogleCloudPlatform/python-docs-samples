#!/usr/bin/env python
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Print each row of the `Albums` table and capture gRPC query metrics including
the round-trip latency.
"""

# [START spanner_opencensus_capture_grpc_metric]

# Modules provided by `google-cloud-spanner`
from google.cloud import spanner

# Modules provided by `opencensus`
from opencensus.stats import aggregation
from opencensus.stats import measure
from opencensus.stats import stats
from opencensus.stats import view
from opencensus.tags import tag_key

# Modules provided by `opencensus-ext-stackdriver`
from opencensus.ext.stackdriver import stats_exporter

# Client-side gRPC metrics, defined in
# https://github.com/census-instrumentation/opencensus-specs/blob/80abe4c67b5322ba6f2254c105d4967f0f46ea99/stats/gRPC.md

# Units
UNIT_COUNT = 1
UNIT_MS = "ms"
UNIT_BYTE = "By"

# Measures
sent_bytes_per_rpc = measure.MeasureInt(
    "grpc.io/client/sent_bytes_per_rpc",
    "Total bytes sent across all request messages per RPC.",
    UNIT_BYTE,
)
received_bytes_per_rpc = measure.MeasureInt(
    "grpc.io/client/received_bytes_per_rpc",
    "Total bytes received across all response messages per RPC.",
    UNIT_BYTE,
)
roundtrip_latency = measure.MeasureInt(
    "grpc.io/client/roundtrip_latency",
    "Time between first byte of request sent to last byte of response received, or terminal error.",
    UNIT_MS,
)
started_rpcs = measure.MeasureInt(
    "grpc.io/client/started_rpcs",
    "The total number of client RPCs ever opened, including those that have not completed.",
    UNIT_COUNT,
)

# Tags
grpc_client_method = tag_key.TagKey("grpc_client_method")
grpc_client_status = tag_key.TagKey("grpc_client_status")

# Default distributions for different measure types
distb_bytes = aggregation.DistributionAggregation(
    [
        1024,
        2048,
        4096,
        16384,
        65536,
        262144,
        1048576,
        4194304,
        16777216,
        67108864,
        268435456,
        1073741824,
        4294967296,
    ]
)
distb_ms = aggregation.DistributionAggregation(
    [
        0.01,
        0.05,
        0.1,
        0.3,
        0.6,
        0.8,
        1,
        2,
        3,
        4,
        5,
        6,
        8,
        10,
        13,
        16,
        20,
        25,
        30,
        40,
        50,
        65,
        80,
        100,
        130,
        160,
        200,
        250,
        300,
        400,
        500,
        650,
        800,
        1000,
        2000,
        5000,
        10000,
        20000,
        50000,
        100000,
    ]
)

# Default views for gRPC metrics, defined in
# https://github.com/census-instrumentation/opencensus-specs/blob/80abe4c67b5322ba6f2254c105d4967f0f46ea99/stats/gRPC.md#default-views
view_bytes_sent_by_method = view.View(
    "grpc.io/client/sent_bytes_per_rpc",
    "Distribution of bytes sent per RPC, by method",
    [grpc_client_method],
    sent_bytes_per_rpc,
    distb_bytes,
)
view_bytes_rcvd_by_method = view.View(
    "grpc.io/client/received_bytes_per_rpc",
    "Distribution of bytes received per RPC, by method",
    [grpc_client_method],
    received_bytes_per_rpc,
    distb_bytes,
)
view_latency_by_method = view.View(
    "grpc.io/client/roundtrip_latency",
    "Distribution of round-trip latency, by method",
    [grpc_client_method],
    roundtrip_latency,
    distb_ms,
)
view_completed_rpcs_by_method_and_status = view.View(
    "grpc.io/client/completed_rpcs",
    "Count of completed RPCs by method and status",
    [grpc_client_method, grpc_client_status],
    roundtrip_latency,
    aggregation.CountAggregation(),
)
view_started_rpcs_by_method = view.View(
    "grpc.io/client/started_rpcs",
    "Count of started RPCs by method",
    [grpc_client_method],
    started_rpcs,
    aggregation.CountAggregation(),
)

# Register the gRPC metrics views
stats.stats.view_manager.register_view(view_bytes_sent_by_method)
stats.stats.view_manager.register_view(view_bytes_rcvd_by_method)
stats.stats.view_manager.register_view(view_latency_by_method)
stats.stats.view_manager.register_view(view_completed_rpcs_by_method_and_status)
stats.stats.view_manager.register_view(view_started_rpcs_by_method)

# Create and register the Stackdriver stats exporter
stackdriver_stats_exporter = stats_exporter.new_stats_exporter()
stats.stats.view_manager.register_exporter(stackdriver_stats_exporter)


def query_with_grpc_metrics(instance_id, database_id):
    """Print each row of the Albums table."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT SingerId, AlbumId, AlbumTitle FROM Albums"
        )

        for row in results:
            print(u"{} {} {}".format(*row))


# [END spanner_opencensus_capture_grpc_metric]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("instance", type=str, help="instance ID")
    parser.add_argument("database", type=str, help="database ID")
    args = parser.parse_args()

    query_with_grpc_metrics(args.instance, args.database)
