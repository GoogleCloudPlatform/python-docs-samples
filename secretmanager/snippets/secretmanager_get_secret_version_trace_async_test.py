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

"""Unit tests for secretmanager_get_secret_version_trace_async snippet."""

import os
from unittest import mock

from google.api_core import _observability
from google.api_core.client_options import ClientOptions
from google.api_core.gapic_v1 import method_async
from google.cloud import secretmanager
from google.cloud.secretmanager_v1.services.secret_manager_service.transports.grpc_asyncio import (
    SecretManagerServiceGrpcAsyncIOTransport,
)
import grpc
import pytest

from secretmanager_get_secret_version_trace_async import (
    get_secret_version_with_tracing_async,
)

# Ensure OTel tracing capabilities are enabled in the environment
os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"
os.environ["GOOGLE_SDK_PYTHON_TRACING_ENABLED"] = "true"


@pytest.mark.asyncio
async def test_get_secret_version_with_tracing_async_spans(
    mock_grpc_server, otel_setup
):
    """Verifies that get_secret_version_with_tracing_async emits T3 and T4 spans."""
    port = mock_grpc_server
    provider, exporter = otel_setup

    orig_init = SecretManagerServiceGrpcAsyncIOTransport.__init__

    def patched_init(self, *args, **kwargs):
        opts = ClientOptions(api_endpoint=f"127.0.0.1:{port}", tracer_provider=provider)
        interceptors = _observability.get_otel_async_interceptor(opts)
        kwargs["channel"] = grpc.aio.insecure_channel(
            f"127.0.0.1:{port}", interceptors=interceptors
        )
        orig_init(self, *args, **kwargs)
        # Ensure modern GAPIC async tracing wrapper is attached
        self._wrapped_methods[self.get_secret_version] = method_async.wrap_method(
            self.get_secret_version,
            method_name="/google.cloud.secretmanager.v1.SecretManagerService/GetSecretVersion",
            client_options=opts,
            kind="grpc_asyncio",
        )

    with mock.patch(
        "secretmanager_get_secret_version_trace_async.TracerProvider",
        return_value=provider,
    ):
        with mock.patch.object(
            SecretManagerServiceGrpcAsyncIOTransport, "__init__", patched_init
        ):
            version = await get_secret_version_with_tracing_async(
                project_id="test-project",
                secret_id="my-secret",
                version_id="1",
            )

    # Verify returned SecretVersion metadata
    assert version.name == "projects/test-project/secrets/my-secret/versions/1"
    assert version.state == secretmanager.SecretVersion.State.ENABLED

    # Inspect emitted spans
    spans = exporter.get_finished_spans()
    assert len(spans) == 2, f"Expected 2 spans (T3 + T4), but got {len(spans)}"

    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]

    assert len(t3_spans) == 1, "Expected exactly 1 T3 (logical method) span"
    assert len(t4_spans) == 1, "Expected exactly 1 T4 (wire attempt) span"

    t3_span = t3_spans[0]
    t4_span = t4_spans[0]

    # Verify T3 logical client span attributes
    assert (
        t3_span.name
        == "google.cloud.secretmanager.v1.SecretManagerService/GetSecretVersion"
    )
    assert t3_span.attributes.get("rpc.system.name") == "grpc"
    assert t3_span.attributes.get("rpc.response.status_code") == "OK"

    # Verify T4 wire attempt span attributes
    assert (
        t4_span.name
        == "google.cloud.secretmanager.v1.SecretManagerService/GetSecretVersion"
    )
    assert (
        t4_span.attributes.get("rpc.service")
        == "google.cloud.secretmanager.v1.SecretManagerService"
    )
    assert t4_span.attributes.get("rpc.grpc.status_code") == 0
    assert t4_span.attributes.get("rpc.response.status_code") == "OK"

    # Verify span hierarchy / parent-child linkage
    assert t4_span.parent.span_id == t3_span.context.span_id
