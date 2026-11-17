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

# [START spanner_opentelemetry_traces_otlp_usage]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ALWAYS_ON
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


def configure_otlp_tracing(project_id: str, instance_id: str, database_id: str) -> None:
    """Configures client-side and end-to-end Spanner tracing via OTLP gRPC.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID.
    """
    set_global_textmap(TraceContextTextMapPropagator())
    tracer_provider = TracerProvider(sampler=ALWAYS_ON)
    otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    observability_options = {
        "tracer_provider": tracer_provider,
        "enable_extended_tracing": True,
        "enable_end_to_end_tracing": True,
    }
    client = spanner.Client(
        project=project_id,
        observability_options=observability_options,
    )
    database = client.instance(instance_id).database(database_id)
    tracer = tracer_provider.get_tracer("spanner-otlp-sample")

    try:
        with tracer.start_as_current_span("VerifySpannerRead"):
            with database.snapshot() as snapshot:
                row = list(snapshot.execute_sql("SELECT 1"))[0]
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"in project '{project_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: OTLP-traced query failed on database '{database_id}' "
            f"in instance '{instance_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        print(f"Check Result: {row[0]}")
        print("End-to-End Tracing: True")
        print("Trace Exporter: OTLP")
    finally:
        tracer_provider.shutdown()


# [END spanner_opentelemetry_traces_otlp_usage]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Configure OpenTelemetry OTLP tracing on a Spanner client."
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

    configure_otlp_tracing(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
