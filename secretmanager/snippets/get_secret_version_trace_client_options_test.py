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

"""Unit tests for get_secret_version_trace_client_options snippet."""

import os
from unittest import mock

from google.api_core.client_options import ClientOptions
from google.api_core.gapic_v1 import method
from google.cloud import secretmanager
from google.cloud.secretmanager_v1.services.secret_manager_service.transports.grpc import (
    SecretManagerServiceGrpcTransport,
)
import grpc

from get_secret_version_trace_client_options import (
    get_secret_version_with_client_options,
)

os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"


def test_get_secret_version_with_client_options(
    mock_grpc_server, otel_setup, monkeypatch
):
    """Verifies that get_secret_version_with_client_options emits spans via ClientOptions."""
    port = mock_grpc_server
    provider, exporter = otel_setup

    orig_init = SecretManagerServiceGrpcTransport.__init__

    def patched_init(self, *args, **kwargs):
        kwargs["channel"] = grpc.insecure_channel(f"127.0.0.1:{port}")
        client_opts = kwargs.get("client_options") or ClientOptions(
            tracer_provider=provider
        )
        orig_init(self, *args, **kwargs)
        if client_opts and client_opts.tracer_provider:
            self._wrapped_methods[self.get_secret_version] = method.wrap_method(
                self.get_secret_version,
                method_name="/google.cloud.secretmanager.v1.SecretManagerService/GetSecretVersion",
                client_options=client_opts,
                kind="grpc",
            )

    monkeypatch.setattr(SecretManagerServiceGrpcTransport, "__init__", patched_init)
    monkeypatch.delenv("GOOGLE_SDK_PYTHON_TRACING_ENABLED", raising=False)

    with mock.patch(
        "get_secret_version_trace_client_options.TracerProvider",
        return_value=provider,
    ):
        version = get_secret_version_with_client_options(
            project_id="test-project",
            secret_id="my-secret",
            version_id="1",
        )

    assert version.name == "projects/test-project/secrets/my-secret/versions/1"
    assert version.state == secretmanager.SecretVersion.State.ENABLED

    spans = exporter.get_finished_spans()
    assert len(spans) >= 1
    t3_span = spans[-1]
    assert "GetSecretVersion" in t3_span.name
    assert t3_span.status.is_ok
