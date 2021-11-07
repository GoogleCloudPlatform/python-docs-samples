"""
# Copyright 2021 Google LLC
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
"""
import random
import time

# [START monitoring_sli_metrics_opencensus_setup]
from flask import Flask
from opencensus.ext.prometheus import stats_exporter as prometheus
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

from prometheus_flask_exporter import PrometheusMetrics

# [END monitoring_sli_metrics_opencensus_setup]

# set up measures
# [START monitoring_sli_metrics_opencensus_measure]
m_request_count = measure_module.MeasureInt(
    "python_request_count", "total requests", "requests"
)
m_failed_request_count = measure_module.MeasureInt(
    "python_failed_request_count", "failed requests", "requests"
)
m_response_latency = measure_module.MeasureFloat(
    "python_response_latency", "response latency", "s"
)
# [END monitoring_sli_metrics_opencensus_measure]

# set up stats recorder
stats_recorder = stats_module.stats.stats_recorder
# [START monitoring_sli_metrics_opencensus_view]
# set up views
latency_view = view_module.View(
    "python_response_latency",
    "The distribution of the latencies",
    [],
    m_response_latency,
    aggregation_module.DistributionAggregation(
        [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    ),
)

request_count_view = view_module.View(
    "python_request_count",
    "total requests",
    [],
    m_request_count,
    aggregation_module.CountAggregation(),
)

failed_request_count_view = view_module.View(
    "python_failed_request_count",
    "failed requests",
    [],
    m_failed_request_count,
    aggregation_module.CountAggregation(),
)


# register views
def register_all_views(view_manager: stats_module.stats.view_manager) -> None:
    view_manager.register_view(latency_view)
    view_manager.register_view(request_count_view)
    view_manager.register_view(failed_request_count_view)
    # [END monitoring_sli_metrics_opencensus_view]


# set up exporter
# [START monitoring_sli_metrics_opencensus_exporter]
def setup_openCensus_and_prometheus_exporter() -> None:
    stats = stats_module.stats
    view_manager = stats.view_manager
    exporter = prometheus.new_stats_exporter(prometheus.Options(namespace="oc_python"))
    view_manager.register_exporter(exporter)
    register_all_views(view_manager)
    # [END monitoring_sli_metrics_opencensus_exporter]


app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/")
def homePage() -> (str, int):
    # start timer
    # [START monitoring_sli_metrics_opencensus_latency]
    start_time = time.perf_counter()
    # [START monitoring_sli_metrics_opencensus_counts]
    mmap = stats_recorder.new_measurement_map()
    # [END monitoring_sli_metrics_opencensus_latency]
    # count request
    mmap.measure_int_put(m_request_count, 1)
    # fail 10% of the time
    # [START monitoring_sli_metrics_opencensus_latency]
    if random.randint(0, 100) > 90:
        # [END monitoring_sli_metrics_opencensus_latency]
        mmap.measure_int_put(m_failed_request_count, 1)
        # [END monitoring_sli_metrics_opencensus_counts]
        # [START monitoring_sli_metrics_opencensus_latency]
        response_latency = time.perf_counter() - start_time
        mmap.measure_float_put(m_response_latency, response_latency)
        # [START monitoring_sli_metrics_opencensus_counts]
        tmap = tag_map_module.TagMap()
        mmap.record(tmap)
        # [END monitoring_sli_metrics_opencensus_latency]
        return ("error!", 500)
        # [END monitoring_sli_metrics_opencensus_counts]
    else:
        random_delay = random.randint(0, 5000) / 1000
        # delay for a bit to vary latency measurement
        time.sleep(random_delay)
        # record latency
        response_latency = time.perf_counter() - start_time
        mmap.measure_float_put(m_response_latency, response_latency)
        tmap = tag_map_module.TagMap()
        mmap.record(tmap)
        return ("home page", 200)


if __name__ == "__main__":
    setup_openCensus_and_prometheus_exporter()
    app.run(port=8080)
