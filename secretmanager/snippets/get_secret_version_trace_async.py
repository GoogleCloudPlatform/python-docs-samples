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

"""Sample demonstrating async OpenTelemetry distributed tracing with SecretManagerServiceAsyncClient."""

# [START secretmanager_enable_tracing_async]
import asyncio
import os

from google.cloud import secretmanager
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


async def get_secret_version_with_tracing_async(
    project_id: str,
    secret_id: str,
    version_id: str = "latest",
) -> secretmanager.SecretVersion:
    """Get a secret version using SecretManagerServiceAsyncClient with OpenTelemetry tracing.

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
    # Initialize the OpenTelemetry TracerProvider with a Console exporter
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)

    # Enable Google Cloud client library tracing
    os.environ["GOOGLE_SDK_PYTHON_TRACING_ENABLED"] = "true"

    # Instantiate the async client
    client = secretmanager.SecretManagerServiceAsyncClient()

    # Construct resource name and invoke the async RPC
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        print("--- OpenTelemetry Trace Spans (JSON) ---")
        response = await client.get_secret_version(request={"name": name})
        state_name = response.state.name
        print(
            f"\nAPI Result: Retrieved secret version {response.name} (state: {state_name})"
        )
        return response
    finally:
        # Flush buffered spans before program completion
        provider.shutdown()


# [END secretmanager_enable_tracing_async]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Get a Secret Manager secret version asynchronously with OpenTelemetry tracing."
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret")
    parser.add_argument(
        "version_id", default="latest", nargs="?", help="version to get"
    )

    args = parser.parse_args()
    asyncio.run(
        get_secret_version_with_tracing_async(
            project_id=args.project_id,
            secret_id=args.secret_id,
            version_id=args.version_id,
        )
    )
