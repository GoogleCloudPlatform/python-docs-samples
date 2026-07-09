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

import main
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider
import pytest
import redis
from redis.exceptions import ConnectionError


def test_smart_redis_call_success():
    """Verifies successful SET and GET execution paths and latency recording."""
    mock_func = mock.MagicMock(return_value="active")
    mock_pool = mock.MagicMock()
    mock_metrics = {
        "client_block_hist": mock.MagicMock(),
        "rtt_hist": mock.MagicMock(),
        "app_block_hist": mock.MagicMock(),
        "retry_counter": mock.MagicMock(),
        "conn_error_counter": mock.MagicMock(),
    }

    result = main.smart_redis_call(
        "set_user",
        mock_func,
        mock_pool,
        mock_metrics,
        "user:123",
        "active",
    )

    assert result == "active"
    mock_func.assert_called_once_with("user:123", "active")

    # Verify all 3 latency histograms were neatly invoked
    mock_metrics["client_block_hist"].record.assert_called_once()
    mock_metrics["rtt_hist"].record.assert_called_once()
    mock_metrics["app_block_hist"].record.assert_called_once()

    # Verify retry counters were untouched
    mock_metrics["retry_counter"].add.assert_not_called()
    mock_metrics["conn_error_counter"].add.assert_not_called()


def test_smart_redis_call_retry_success():
    """Simulates 2 sequential connectivity failures followed by 3rd attempt success."""
    mock_func = mock.MagicMock(
        side_effect=[
            ConnectionError("cluster unreachable attempt 1"),
            ConnectionError("cluster unreachable attempt 2"),
            "success_response",
        ]
    )
    mock_pool = mock.MagicMock()
    mock_metrics = {
        "client_block_hist": mock.MagicMock(),
        "rtt_hist": mock.MagicMock(),
        "app_block_hist": mock.MagicMock(),
        "retry_counter": mock.MagicMock(),
        "conn_error_counter": mock.MagicMock(),
    }

    # Wrap in a sleep patch so the test suite runs in milliseconds
    with mock.patch("time.sleep", return_value=None):
        result = main.smart_redis_call(
            "get_user",
            mock_func,
            mock_pool,
            mock_metrics,
            "user:123",
        )

    assert result == "success_response"
    assert mock_func.call_count == 3

    # Verify counters captured exactly 2 retry events
    assert mock_metrics["retry_counter"].add.call_count == 2
    assert mock_metrics["conn_error_counter"].add.call_count == 2
    mock_metrics["retry_counter"].add.assert_called_with(
        1, {"operation": "get_user"}
    )
    mock_metrics["conn_error_counter"].add.assert_called_with(
        1, {"operation": "get_user"}
    )

    # Success on 3rd attempt means latency was recorded
    mock_metrics["app_block_hist"].record.assert_called_once()


def test_smart_redis_call_permanent_failure():
    """Verifies that permanent connectivity failures bubble up after 3 attempts."""
    mock_func = mock.MagicMock(
        side_effect=ConnectionError("permanent DNS error")
    )
    mock_pool = mock.MagicMock()
    mock_metrics = {
        "client_block_hist": mock.MagicMock(),
        "rtt_hist": mock.MagicMock(),
        "app_block_hist": mock.MagicMock(),
        "retry_counter": mock.MagicMock(),
        "conn_error_counter": mock.MagicMock(),
    }

    with mock.patch("time.sleep", return_value=None):
        with pytest.raises(ConnectionError) as exc_info:
            main.smart_redis_call(
                "set_user",
                mock_func,
                mock_pool,
                mock_metrics,
                "user:123",
                "active",
            )

    assert "permanent DNS error" in str(exc_info.value)
    assert mock_func.call_count == 3

    # Verify all 3 attempts were tracked
    assert mock_metrics["retry_counter"].add.call_count == 3
    assert mock_metrics["conn_error_counter"].add.call_count == 3

    # Verify latency was NOT recorded on a permanent failure
    mock_metrics["app_block_hist"].record.assert_not_called()


def test_init_redis_pool_live(monkeypatch):
    """Verifies init_redis_pool correctly parses environment variables without network calls."""
    monkeypatch.setenv("REDISHOST", "10.0.0.1")
    monkeypatch.setenv("REDISPORT", "7000")

    redis_pool, redis_client = main.init_redis_pool()

    assert redis_pool is not None
    assert redis_client is not None
    assert redis_pool.connection_kwargs["host"] == "10.0.0.1"
    assert redis_pool.connection_kwargs["port"] == 7000

    # Test default fallback
    monkeypatch.delenv("REDISHOST", raising=False)
    monkeypatch.delenv("REDISPORT", raising=False)

    pool_def, r_def = main.init_redis_pool()
    assert pool_def.connection_kwargs["host"] == "localhost"
    assert pool_def.connection_kwargs["port"] == 6379


def test_smart_redis_call_live_or_skip():
    """Integration Test: Hits a real Redis endpoint if running locally at localhost:6379."""
    import main as live_main
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.trace import TracerProvider
    import pytest
    import redis

    # Initialize REAL No-op OpenTelemetry SDK providers (invoked directly)
    TracerProvider()
    mp = MeterProvider()

    try:
        # Exercise actual pool creation and connectivity ping
        redis_pool, redis_client = live_main.init_redis_pool()
        redis_client.ping()
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
        pytest.skip(
            "Skipping live Redis test: No running server found at localhost:6379"
        )

    # Bind all 5 real OpenTelemetry No-op metrics for this live execution block
    meter = mp.get_meter("test_redis_live")
    live_metrics = {
        "client_block_hist": meter.create_histogram("client_block"),
        "rtt_hist": meter.create_histogram("rtt_hist"),
        "app_block_hist": meter.create_histogram("app_block"),
        "retry_counter": meter.create_counter("retry_count"),
        "conn_error_counter": meter.create_counter("conn_error"),
    }

    try:
        # Run a real Redis write hitting the ACTUAL endpoint (invoked directly)
        live_main.smart_redis_call(
            "set_test",
            redis_client.set,
            redis_pool,
            live_metrics,
            "test:key",
            "live_val",
        )

        result_get = live_main.smart_redis_call(
            "get_test",
            redis_client.get,
            redis_pool,
            live_metrics,
            "test:key",
        )

        assert result_get == "live_val"

        # Safe DB Cleanup
        redis_client.delete("test:key")

    finally:
        redis_pool.disconnect()


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
    """Verifies the init_telemetry function correctly instruments Redis."""
    tracer, redis_metrics, tp, mp = main.init_telemetry()

    assert tracer is not None
    assert redis_metrics is not None
    assert tp is not None
    assert mp is not None
    assert "rtt_hist" in redis_metrics
    assert "app_block_hist" in redis_metrics
    assert "client_block_hist" in redis_metrics

    mock_redis_instrumentor.return_value.instrument.assert_called_once()
    mock_cloud_trace.assert_called_once()
    mock_cloud_metrics.assert_called_once()