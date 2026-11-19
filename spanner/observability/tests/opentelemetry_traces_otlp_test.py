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

import runpy
from unittest import mock

from google.api_core import exceptions
from google.cloud import spanner
from opentelemetry.sdk.trace.export import SpanExportResult
import pytest
from spanner_observability import opentelemetry_traces_otlp

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"
OTLP_EXPORTER = "spanner_observability.opentelemetry_traces_otlp.OTLPSpanExporter"
OTLP_EXPORTER_SRC = (
    "opentelemetry.exporter.otlp.proto.grpc.trace_exporter.OTLPSpanExporter"
)


@mock.patch(OTLP_EXPORTER)
@mock.patch(SPANNER_CLIENT)
def test_configure_otlp_tracing_success(
    mock_client_class: mock.MagicMock,
    mock_exporter_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_exporter_class.return_value.export.return_value = SpanExportResult.SUCCESS
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [(1,)]

    opentelemetry_traces_otlp.configure_otlp_tracing(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    obs = mock_client_class.call_args.kwargs["observability_options"]
    assert obs["enable_end_to_end_tracing"] is True
    assert obs["enable_extended_tracing"] is True
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Check Result: 1" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("db missing"),
            "error: database 'example-db' on instance 'example-instance'",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: OTLP-traced query failed",
        ),
    ],
)
@mock.patch(OTLP_EXPORTER)
@mock.patch(SPANNER_CLIENT)
def test_configure_otlp_tracing_errors(
    mock_client_class: mock.MagicMock,
    mock_exporter_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_exporter_class.return_value.export.return_value = SpanExportResult.SUCCESS
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.side_effect = error

    opentelemetry_traces_otlp.configure_otlp_tracing(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(OTLP_EXPORTER_SRC)
@mock.patch(SPANNER_CLIENT)
def test_configure_otlp_tracing_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    mock_exporter_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_exporter_class.return_value.export.return_value = SpanExportResult.SUCCESS
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [(1,)]
    monkeypatch.setattr(
        "sys.argv",
        [
            "opentelemetry_traces_otlp.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_observability.opentelemetry_traces_otlp", run_name="__main__"
    )

    assert "Check Result: 1" in capsys.readouterr().out


@conftest.live_only
def test_configure_otlp_tracing_live(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        mock.patch(OTLP_EXPORTER) as mock_exp,
        mock.patch.object(spanner, "Client", wraps=spanner.Client) as spy_client,
    ):
        mock_exp.return_value.export.return_value = SpanExportResult.SUCCESS
        opentelemetry_traces_otlp.configure_otlp_tracing(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )

    obs = spy_client.call_args.kwargs["observability_options"]
    assert obs["enable_end_to_end_tracing"] is True
    assert obs["enable_extended_tracing"] is True
    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert "Check Result: 1" in out
