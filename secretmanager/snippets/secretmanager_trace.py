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

"""Sample demonstrating OpenTelemetry distributed tracing with SecretManagerServiceClient."""

# [START secretmanager_enable_tracing]
import os

from google.cloud import secretmanager
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


def access_secret_version_with_tracing(
    project_id: str,
    secret_id: str,
    version_id: str = "latest",
) -> str:
    """Access a secret version in Secret Manager with OpenTelemetry tracing enabled.

    Args:
        project_id: Google Cloud project ID.
        secret_id: ID of the secret to access.
        version_id: ID of the secret version to access (defaults to "latest").

    Returns:
        The secret payload decoded as a UTF-8 string.
    """
    # NOTE: In standalone scripts or CLI tools, initialize and shut down the
    # TracerProvider within the script workflow. In long-running production
    # applications (e.g., web servers), configure the TracerProvider once at
    # application startup.
    #
    # 1. Initialize the OpenTelemetry TracerProvider with a Console exporter
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)

    # 2. Enable Google Cloud client library tracing
    os.environ["GOOGLE_SDK_PYTHON_TRACING_ENABLED"] = "true"

    # 3. Instantiate the client (automatically discovers the active TracerProvider)
    client = secretmanager.SecretManagerServiceClient()

    # 4. Construct the resource name and invoke the RPC
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return payload
    finally:
        # Flush buffered spans before program completion
        provider.shutdown()


# [END secretmanager_enable_tracing]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Access a Secret Manager secret version with OpenTelemetry tracing."
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to access")
    parser.add_argument(
        "version_id", default="latest", nargs="?", help="version to access"
    )

    args = parser.parse_args()
    secret_data = access_secret_version_with_tracing(
        project_id=args.project_id,
        secret_id=args.secret_id,
        version_id=args.version_id,
    )
    print(f"Retrieved secret payload: {secret_data}")
