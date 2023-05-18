#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
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

# [START monitoring_opencensus_metrics_quickstart]

from random import random
import time

from opencensus.ext.stackdriver import stats_exporter
from opencensus.stats import aggregation
from opencensus.stats import measure
from opencensus.stats import stats
from opencensus.stats import view


# A measure that represents task latency in ms.
LATENCY_MS = measure.MeasureFloat(
    "task_latency",
    "The task latency in milliseconds",
    "ms")

# A view of the task latency measure that aggregates measurements according to
# a histogram with predefined bucket boundaries. This aggregate is periodically
# exported to Stackdriver Monitoring.
LATENCY_VIEW = view.View(
    "task_latency_distribution",
    "The distribution of the task latencies",
    [],
    LATENCY_MS,
    # Latency in buckets: [>=0ms, >=100ms, >=200ms, >=400ms, >=1s, >=2s, >=4s]
    aggregation.DistributionAggregation(
        [100.0, 200.0, 400.0, 1000.0, 2000.0, 4000.0]))


def main():
    # Register the view. Measurements are only aggregated and exported if
    # they're associated with a registered view.
    stats.stats.view_manager.register_view(LATENCY_VIEW)

    # Create the Stackdriver stats exporter and start exporting metrics in the
    # background, once every 60 seconds by default.
    exporter = stats_exporter.new_stats_exporter()
    print('Exporting stats to project "{}"'
          .format(exporter.options.project_id))

    # Register exporter to the view manager.
    stats.stats.view_manager.register_exporter(exporter)

    # Record 100 fake latency values between 0 and 5 seconds.
    for num in range(100):
        ms = random() * 5 * 1000

        mmap = stats.stats.stats_recorder.new_measurement_map()
        mmap.measure_float_put(LATENCY_MS, ms)
        mmap.record()

        print(f"Fake latency recorded ({num}: {ms})")

    # Keep the thread alive long enough for the exporter to export at least
    # once.
    time.sleep(65)


if __name__ == '__main__':
    main()

# [END monitoring_opencensus_metrics_quickstart]
