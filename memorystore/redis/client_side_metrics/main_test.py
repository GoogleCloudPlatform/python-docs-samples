# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

from opentelemetry.instrumentation.redis import RedisInstrumentor
import pytest
from redis.exceptions import ConnectionError

import main


@pytest.fixture
def mock_telemetry(monkeypatch):
    """Hermetically binds mock OpenTelemetry and Pool globals for the duration of the test."""
    mock_tracer = mock.MagicMock()
    mock_rtt = mock.MagicMock()
    mock_client = mock.MagicMock()
    mock_app = mock.MagicMock()
    mock_retry = mock.MagicMock()
    mock_conn_err = mock.MagicMock()
    mock_pool = mock.MagicMock()

    # Prevent real time.sleep calls during retry handling to make tests lightning fast
    monkeypatch.setattr(main.time, "sleep", lambda x: None)

    monkeypatch.setattr(main, "tracer", mock_tracer)
    monkeypatch.setattr(main, "rtt_hist", mock_rtt)
    monkeypatch.setattr(main, "client_block_hist", mock_client)
    monkeypatch.setattr(main, "app_block_hist", mock_app)
    monkeypatch.setattr(main, "retry_counter", mock_retry)
    monkeypatch.setattr(main, "conn_error_counter", mock_conn_err)
    monkeypatch.setattr(main, "pool", mock_pool)

    return {
        "rtt_hist": mock_rtt,
        "client_block_hist": mock_client,
        "app_block_hist": mock_app,
        "retry_counter": mock_retry,
        "conn_error_counter": mock_conn_err,
        "pool": mock_pool,
    }


def test_smart_redis_call_success(mock_telemetry):
    """Verifies standard successful SET and GET execution paths and latency recording."""
    mock_func = mock.MagicMock(return_value="active")

    result = main.smart_redis_call("set_user", mock_func, "user:123", "active")

    assert result == "active"
    mock_func.assert_called_once_with("user:123", "active")
    mock_telemetry["pool"].get_connection.assert_called_once_with("PING")
    mock_telemetry["pool"].release.assert_called_once()

    # Verify all metrics were cleanly invoked
    mock_telemetry["client_block_hist"].record.assert_called_once()
    mock_telemetry["rtt_hist"].record.assert_called_once()
    mock_telemetry["app_block_hist"].record.assert_called_once()

    # Verify retry counters were untouched
    mock_telemetry["retry_counter"].add.assert_not_called()
    mock_telemetry["conn_error_counter"].add.assert_not_called()


def test_smart_redis_call_retry_success(mock_telemetry):
    """Simulates 2 sequential connectivity failures followed by a successful 3rd retry."""
    mock_func = mock.MagicMock(
        side_effect=[
            ConnectionError("cluster unreachable attempt 1"),
            ConnectionError("cluster unreachable attempt 2"),
            "success_response",
        ]
    )

    result = main.smart_redis_call("get_user", mock_func, "user:123")

    assert result == "success_response"
    assert mock_func.call_count == 3

    # Verify counters captured exactly 2 retry events
    assert mock_telemetry["retry_counter"].add.call_count == 2
    assert mock_telemetry["conn_error_counter"].add.call_count == 2

    # Expect calls with increment of 1 and proper operation attribute
    mock_telemetry["retry_counter"].add.assert_called_with(
        1, {"operation": "get_user"}
    )
    mock_telemetry["conn_error_counter"].add.assert_called_with(
        1, {"operation": "get_user"}
    )

    # Success on 3rd attempt means round-trip latency was recorded
    mock_telemetry["rtt_hist"].record.assert_called_once()


def test_smart_redis_call_permanent_failure(mock_telemetry):
    """Verifies that permanent connectivity failures bubble up and trigger exactly 3 attempts."""
    mock_func = mock.MagicMock(
        side_effect=ConnectionError("permanent DNS error")
    )

    with pytest.raises(ConnectionError) as exc_info:
        main.smart_redis_call("set_user", mock_func, "user:123", "active")

    assert "permanent DNS error" in str(exc_info.value)
    assert mock_func.call_count == 3

    # Verify all 3 attempts were tracked
    assert mock_telemetry["retry_counter"].add.call_count == 3
    assert mock_telemetry["conn_error_counter"].add.call_count == 3


@mock.patch("main.BatchSpanProcessor")
@mock.patch("main.PeriodicExportingMetricReader")
@mock.patch("main.CloudTraceSpanExporter")
@mock.patch("main.CloudMonitoringMetricsExporter")
@mock.patch("main.RedisInstrumentor")
def test_init_telemetry_mocks(
    mock_redis_instrumentor,
    mock_cloud_metrics,
    mock_cloud_trace,
    mock_metric_reader,
    mock_span_processor,
):
    """Verifies the init_telemetry function cleanly instruments Redis and the OTel SDK."""
    tp, mp = main.init_telemetry()

    assert tp is not None
    assert mp is not None
    mock_redis_instrumentor.return_value.instrument.assert_called_once()
    mock_cloud_trace.assert_called_once()
    mock_cloud_metrics.assert_called_once()