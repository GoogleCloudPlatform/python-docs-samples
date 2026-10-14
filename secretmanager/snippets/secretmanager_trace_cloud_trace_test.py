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

"""Unit tests for secretmanager_trace_cloud_trace snippet."""

import concurrent.futures
import os
import sys
from unittest import mock

from google.cloud import secretmanager
from google.cloud.secretmanager_v1.services.secret_manager_service.transports.grpc import (
    SecretManagerServiceGrpcTransport,
)
import grpc
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
import pytest


# Mock opentelemetry.exporter.cloud_trace if not installed in the environment
class MockCloudTraceSpanExporter(SpanExporter):
    def __init__(self, *args, **kwargs):
        self.exported_spans = []

    def export(self, spans):
        self.exported_spans.extend(spans)
        return SpanExportResult.SUCCESS

    def shutdown(self):
        pass


if "opentelemetry.exporter.cloud_trace" not in sys.modules:
    mock_module = mock.MagicMock()
    mock_module.CloudTraceSpanExporter = MockCloudTraceSpanExporter
    sys.modules["opentelemetry.exporter.cloud_trace"] = mock_module

# flake8: E402 is ignored here because we must patch sys.modules with a mock
# CloudTraceSpanExporter before importing the snippet module in environments
# where opentelemetry-exporter-gcp-trace is not installed.
from secretmanager_trace_cloud_trace import (  # noqa: E402
    access_secret_version_cloud_trace,
)

os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"
os.environ["GOOGLE_SDK_PYTHON_TRACING_ENABLED"] = "true"


@pytest.fixture
def mock_grpc_server():
    """Starts an in-memory gRPC server returning mock responses."""
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=2))
    port = server.add_insecure_port("127.0.0.1:0")

    mock_resp = secretmanager.AccessSecretVersionResponse(
        name="projects/test-project/secrets/my-secret/versions/1",
        payload=secretmanager.SecretPayload(data=b"mock-cloud-trace-secret"),
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


def test_access_secret_version_cloud_trace(mock_grpc_server, monkeypatch):
    """Verifies that access_secret_version_cloud_trace initializes CloudTraceSpanExporter and runs."""
    port = mock_grpc_server

    orig_init = SecretManagerServiceGrpcTransport.__init__

    def patched_init(self, *args, **kwargs):
        kwargs["channel"] = grpc.insecure_channel(f"127.0.0.1:{port}")
        orig_init(self, *args, **kwargs)

    monkeypatch.setattr(SecretManagerServiceGrpcTransport, "__init__", patched_init)

    with mock.patch(
        "secretmanager_trace_cloud_trace.CloudTraceSpanExporter"
    ) as mock_cloud_exporter_cls:
        instance = MockCloudTraceSpanExporter()
        mock_cloud_exporter_cls.return_value = instance

        payload = access_secret_version_cloud_trace(
            project_id="test-project",
            secret_id="my-secret",
            version_id="1",
        )

        assert payload == "mock-cloud-trace-secret"
        mock_cloud_exporter_cls.assert_called_once()
