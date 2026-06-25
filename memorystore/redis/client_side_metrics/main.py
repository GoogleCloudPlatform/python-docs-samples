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

# [START memorystore_redis_client_side_metrics]
import os
import time

from opentelemetry import metrics, trace
from opentelemetry.exporter.cloud_monitoring import CloudMonitoringMetricsExporter
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import redis
from redis.exceptions import ConnectionError, TimeoutError

# 1. Initialize Tracing
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(BatchSpanProcessor(CloudTraceSpanExporter()))
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer("redis.client")

# 2. Initialize Metrics
metrics_exporter = CloudMonitoringMetricsExporter()
metric_reader = PeriodicExportingMetricReader(metrics_exporter, export_interval_millis=10000)
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("redis.metrics")

rtt_hist = meter.create_histogram("redis_client_rtt", unit="ms")
client_block_hist = meter.create_histogram("redis_client_blocking_latency", unit="ms")
app_block_hist = meter.create_histogram("redis_application_blocking_latency", unit="ms")
retry_counter = meter.create_counter("redis_retry_count")
conn_error_counter = meter.create_counter("redis_connectivity_error_count")

retry_counter.add(0, {"operation": "startup"})
conn_error_counter.add(0, {"operation": "startup"})

# 3. Setup Redis
RedisInstrumentor().instrument()
redis_host = os.environ.get("REDISHOST", "localhost")
redis_port = int(os.environ.get("REDISPORT", 6379))

pool = redis.ConnectionPool(host=redis_host, port=redis_port, max_connections=10, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def smart_redis_call(operation_name, func, *args, **kwargs):
    max_retries = 3
    attempt = 0

    pool_start = time.time()
    try:
        conn = pool.get_connection('PING')
        pool.release(conn)
    except Exception:
        pass
    client_block_hist.record((time.time() - pool_start) * 1000, {"operation": operation_name})

    while attempt < max_retries:
        try:
            req_start = time.time()
            response = func(*args, **kwargs)
            rtt_hist.record((time.time() - req_start) * 1000, {"operation": operation_name})

            app_start = time.time()
            _ = str(response)
            app_block_hist.record((time.time() - app_start) * 1000, {"operation": operation_name})

            return response

        except (ConnectionError, TimeoutError) as e:
            attempt += 1
            conn_error_counter.add(1, {"operation": operation_name})
            retry_counter.add(1, {"operation": operation_name})
            if attempt >= max_retries:
                raise e
            time.sleep((2 ** attempt) * 0.1)

if __name__ == "__main__":
    with tracer.start_as_current_span("process_user_span"):
        try:
            # Simple write and read operations
            smart_redis_call("set_user", r.set, "user:123", "active")

            result = smart_redis_call("get_user", r.get, "user:123")
            print(f"Retrieved: {result}")
        except Exception as e:
            print(f"Error: {e}")

    tracer_provider.force_flush()
    meter_provider.force_flush()
# [END memorystore_redis_client_side_metrics]
