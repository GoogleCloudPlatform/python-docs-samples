# -*- coding: utf-8 -*-
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

"""Sample demonstrating exporting OpenTelemetry traces to Google Cloud Trace with SecretManagerServiceClient."""

# [START secretmanager_trace_cloud_trace]
import os

from google.cloud import secretmanager
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)


def get_secret_version_cloud_trace(
    project_id: str,
    secret_id: str,
    version_id: str = "latest",
) -> secretmanager.SecretVersion:
    """Get a secret version in Secret Manager exporting traces to Google Cloud Trace.

    Args:
        project_id: Google Cloud project ID.
        secret_id: ID of the secret.
        version_id: ID of the secret version (defaults to "latest").

    Returns:
        The SecretVersion metadata object.
    """
    # NOTE: In standalone scripts or CLI tools, initialize and shut down the
    # TracerProvider within the script workflow. In long-running production
    # applications (e.g., web servers), configure the TracerProvider once at
    # application startup.
    #
    # Initialize OpenTelemetry TracerProvider with CloudTraceSpanExporter
    # NOTE: We also initialize ConsoleSpanExporter to display results from this sample directly.
    provider = TracerProvider()
    cloud_exporter = CloudTraceSpanExporter()
    provider.add_span_processor(BatchSpanProcessor(cloud_exporter))
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)

    # Enable Google Cloud client library tracing
    os.environ["GOOGLE_SDK_PYTHON_TRACING_ENABLED"] = "true"

    # Instantiate the client (automatically discovers the active TracerProvider)
    client = secretmanager.SecretManagerServiceClient()

    # Construct resource name and invoke RPC
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        print("--- OpenTelemetry Trace Spans (JSON) ---")
        response = client.get_secret_version(request={"name": name})
        state_name = response.state.name
        print(
            f"\nAPI Result: Retrieved secret version {response.name} (state: {state_name})"
        )
        return response
    finally:
        # Flush buffered spans to Cloud Trace before exiting
        provider.shutdown()


# [END secretmanager_trace_cloud_trace]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Get a Secret Manager secret version and export traces to Google Cloud Trace."
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret")
    parser.add_argument(
        "version_id", default="latest", nargs="?", help="version to get"
    )

    args = parser.parse_args()
    get_secret_version_cloud_trace(
        project_id=args.project_id,
        secret_id=args.secret_id,
        version_id=args.version_id,
    )
