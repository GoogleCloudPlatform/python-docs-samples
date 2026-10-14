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

"""Unit tests for secretmanager_trace_client_options snippet."""

import concurrent.futures
import os
from unittest import mock

from google.api_core.gapic_v1 import method
from google.cloud import secretmanager
from google.cloud.secretmanager_v1.services.secret_manager_service.transports.grpc import (
    SecretManagerServiceGrpcTransport,
)
import grpc
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)
import pytest

from secretmanager_trace_client_options import access_secret_version_with_client_options

os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"


@pytest.fixture
def mock_grpc_server():
    """Starts an in-memory gRPC server returning mock responses."""
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=2))
    port = server.add_insecure_port("127.0.0.1:0")

    mock_resp = secretmanager.AccessSecretVersionResponse(
        name="projects/test-project/secrets/my-secret/versions/1",
        payload=secretmanager.SecretPayload(data=b"mock-client-options-token"),
    )

    generic_handler = grpc.method_handlers_generic_handler(
        "google.cloud.secretmanager.v1.SecretManagerService",
        {
            "AccessSecretVersion": grpc.unary_unary_rpc_method_handler(
                lambda r, c: secretmanager.AccessSecretVersionResponse.serialize(
                    mock_resp
                ),
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


def test_access_secret_version_with_client_options(mock_grpc_server, monkeypatch):
    """Verifies that access_secret_version_with_client_options emits spans via ClientOptions."""
    port = mock_grpc_server
    provider = TracerProvider()
    exporter = InMemorySpanExporter()
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    orig_init = SecretManagerServiceGrpcTransport.__init__

    def patched_init(self, *args, **kwargs):
        kwargs["channel"] = grpc.insecure_channel(f"127.0.0.1:{port}")
        client_opts = kwargs.get("client_options")
        orig_init(self, *args, **kwargs)
        if client_opts and client_opts.tracer_provider:
            self._wrapped_methods[self.access_secret_version] = method.wrap_method(
                self.access_secret_version,
                method_name="/google.cloud.secretmanager.v1.SecretManagerService/AccessSecretVersion",
                client_options=client_opts,
                kind="grpc",
            )

    monkeypatch.setattr(SecretManagerServiceGrpcTransport, "__init__", patched_init)
    monkeypatch.delenv("GOOGLE_SDK_PYTHON_TRACING_ENABLED", raising=False)

    with mock.patch(
        "secretmanager_trace_client_options.TracerProvider", return_value=provider
    ):
        payload = access_secret_version_with_client_options(
            project_id="test-project",
            secret_id="my-secret",
            version_id="1",
        )

    assert payload == "mock-client-options-token"

    spans = exporter.get_finished_spans()
    assert len(spans) >= 1
    t3_span = spans[-1]
    assert "AccessSecretVersion" in t3_span.name
    assert t3_span.status.is_ok
