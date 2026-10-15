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

"""Sample demonstrating programmatic OpenTelemetry configuration via ClientOptions with SecretManagerServiceClient."""

# [START secretmanager_trace_client_options]
from google.api_core.client_options import ClientOptions
from google.cloud import secretmanager
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


def access_secret_version_with_client_options(
    project_id: str,
    secret_id: str,
    version_id: str = "latest",
) -> str:
    """Access a secret version configuring tracing programmatically via ClientOptions.

    Args:
        project_id: Google Cloud project ID.
        secret_id: ID of the secret to access.
        version_id: ID of the secret version to access (defaults to "latest").

    Returns:
        The resource name of the accessed secret version.
    """
    # 1. Initialize an independent TracerProvider (no global registration required)
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    # 2. Pass the TracerProvider directly via ClientOptions
    # Tracing is activated specifically for this client instance, even without
    # setting the GOOGLE_SDK_PYTHON_TRACING_ENABLED environment variable.
    options = ClientOptions(tracer_provider=provider)
    client = secretmanager.SecretManagerServiceClient(client_options=options)

    # 3. Construct resource name and invoke RPC
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
        return response.name
    finally:
        # Flush buffered spans before program completion
        provider.shutdown()


# [END secretmanager_trace_client_options]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Access a Secret Manager secret version with ClientOptions-configured tracing."
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to access")
    parser.add_argument(
        "version_id", default="latest", nargs="?", help="version to access"
    )

    args = parser.parse_args()
    access_secret_version_with_client_options(
        project_id=args.project_id,
        secret_id=args.secret_id,
        version_id=args.version_id,
    )
