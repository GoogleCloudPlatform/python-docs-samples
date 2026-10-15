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

"""Shared test fixtures for Secret Manager tracing snippets."""

import concurrent.futures

from google.cloud import secretmanager
import grpc
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)
import pytest


@pytest.fixture(autouse=True)
def reset_otel_global_tracer_provider():
    """Resets OpenTelemetry's global TracerProvider between tests."""
    yield
    trace._TRACER_PROVIDER_SET_ONCE._done = False
    trace._TRACER_PROVIDER = None


@pytest.fixture
def mock_grpc_server():
    """Starts an in-memory gRPC server returning mock responses."""
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=2))
    port = server.add_insecure_port("127.0.0.1:0")

    mock_resp = secretmanager.SecretVersion(
        name="projects/test-project/secrets/my-secret/versions/1",
        state=secretmanager.SecretVersion.State.ENABLED,
    )

    generic_handler = grpc.method_handlers_generic_handler(
        "google.cloud.secretmanager.v1.SecretManagerService",
        {
            "GetSecretVersion": grpc.unary_unary_rpc_method_handler(
                lambda r, c: secretmanager.SecretVersion.serialize(mock_resp),
                request_deserializer=lambda b: b,
                response_serializer=lambda b: b,
            )
        },
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.start()
    try:
        yield port
    finally:
        server.stop(grace=None)


@pytest.fixture
def otel_setup():
    """Configures an in-memory OpenTelemetry tracer provider and exporter."""
    provider = TracerProvider()
    exporter = InMemorySpanExporter()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    return provider, exporter
