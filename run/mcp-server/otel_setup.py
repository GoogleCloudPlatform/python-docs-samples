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

# [START cloudrun_mcpserver_setup_otel]
import logging
import google.auth
import google.auth.transport.requests
import grpc
from google.auth.transport.grpc import AuthMetadataPlugin
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logger = logging.getLogger(__name__)


def setup_opentelemetry(service_name: str) -> None:
    """Sets up OpenTelemetry to send traces to Google Cloud Observability."""
    credentials, project_id = google.auth.default()
    if not project_id:
        raise Exception("Could not determine Google Cloud project ID.")

    resource = Resource.create(
        attributes={
            SERVICE_NAME: service_name,
            "gcp.project_id": project_id,
        }
    )

    # Set up OTLP auth
    request = google.auth.transport.requests.Request()
    auth_metadata_plugin = AuthMetadataPlugin(credentials=credentials, request=request)
    channel_creds = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(),
        grpc.metadata_call_credentials(auth_metadata_plugin),
    )

    # Set up OpenTelemetry Python SDK
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                credentials=channel_creds,
                endpoint="https://telemetry.googleapis.com:443/v1/traces",
            )
        )
    )
    trace.set_tracer_provider(tracer_provider)
    logger.info("OpenTelemetry successfully initialized.")


# [END cloudrun_mcpserver_setup_otel]
