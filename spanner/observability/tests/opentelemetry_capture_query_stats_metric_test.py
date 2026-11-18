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
from opentelemetry.sdk.metrics.export import MetricExportResult
import pytest
from spanner_observability import opentelemetry_capture_query_stats_metric

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"
OTLP_METRIC_EXPORTER = (
    "spanner_observability.opentelemetry_capture_query_stats_metric.OTLPMetricExporter"
)
OTLP_METRIC_EXPORTER_SRC = (
    "opentelemetry.exporter.otlp.proto.grpc.metric_exporter.OTLPMetricExporter"
)


def _mock_profiled_result(
    rows: list[tuple[object, ...]], elapsed: str
) -> mock.MagicMock:
    rs = mock.MagicMock()
    rs.__iter__.return_value = iter(rows)
    rs.stats.query_stats = {"elapsed_time": elapsed}
    return rs


def _configure_mock_exporter(mock_exporter_class: mock.MagicMock) -> None:
    exp = mock_exporter_class.return_value
    exp.export.return_value = MetricExportResult.SUCCESS
    exp._preferred_temporality = {}
    exp._preferred_aggregation = {}


@mock.patch(OTLP_METRIC_EXPORTER)
@mock.patch(SPANNER_CLIENT)
def test_capture_query_stats_metric_success(
    mock_client_class: mock.MagicMock,
    mock_exporter_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _configure_mock_exporter(mock_exporter_class)
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = _mock_profiled_result(
        [(1, "Marc")], "2.50 msecs"
    )

    opentelemetry_capture_query_stats_metric.capture_query_stats_metric(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Elapsed Milliseconds: 2.50" in out
    assert "Metric Name: spanner/query_stats_elapsed" in out
    assert "Row Count: 1" in out
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
            "error: profiled query failed",
        ),
    ],
)
@mock.patch(OTLP_METRIC_EXPORTER)
@mock.patch(SPANNER_CLIENT)
def test_capture_query_stats_metric_errors(
    mock_client_class: mock.MagicMock,
    mock_exporter_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    _configure_mock_exporter(mock_exporter_class)
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.side_effect = error

    opentelemetry_capture_query_stats_metric.capture_query_stats_metric(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(OTLP_METRIC_EXPORTER_SRC)
@mock.patch(SPANNER_CLIENT)
def test_capture_query_stats_metric_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    mock_exporter_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _configure_mock_exporter(mock_exporter_class)
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = _mock_profiled_result(
        [(1, "Marc")], "1.20 msecs"
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "opentelemetry_capture_query_stats_metric.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_observability.opentelemetry_capture_query_stats_metric",
        run_name="__main__",
    )

    assert "Metric Name: spanner/query_stats_elapsed" in capsys.readouterr().out


@conftest.live_only
def test_capture_query_stats_metric_live(capsys: pytest.CaptureFixture[str]) -> None:
    with mock.patch(OTLP_METRIC_EXPORTER) as mock_exp:
        _configure_mock_exporter(mock_exp)
        opentelemetry_capture_query_stats_metric.capture_query_stats_metric(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Metric Name: spanner/query_stats_elapsed" in out
    assert "Row Count:" in out
