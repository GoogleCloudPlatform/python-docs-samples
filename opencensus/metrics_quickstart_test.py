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

from unittest import mock
import unittest

from opencensus.ext.stackdriver import stats_exporter
from opencensus.stats import aggregation
from opencensus.stats import measure
from opencensus.stats import stats
from opencensus.stats import view


class TestMetricsQuickstart(unittest.TestCase):
    """Sanity checks for the OpenCensus metrics quickstart examples.

    These tests check that a few basic features of the library work as expected
    in order for the demo to run. See the opencensus and
    opencensus-ext-stackdriver source for actual library tests.
    """
    @staticmethod
    def test_measure_creation():
        measure.MeasureFloat(
            "task_latency",
            "The task latency in milliseconds",
            "ms")

    @staticmethod
    def test_view_creation():
        test_view = view.View(
            "task_latency_distribution",
            "The distribution of the task latencies",
            [],
            mock.Mock(),
            aggregation.DistributionAggregation([1.0, 2.0, 3.0]))
        # Check that metric descriptor conversion doesn't crash
        test_view.get_metric_descriptor()

    # Don't modify global stats
    @mock.patch('opencensus.ext.stackdriver.stats_exporter.stats.stats',
                stats._Stats())
    def test_measurement_map_record(self):
        mock_measure = mock.Mock()
        mock_measure_name = mock.Mock()
        mock_measure.name = mock_measure_name
        mock_view = mock.Mock()
        mock_view.columns = []
        mock_view.measure = mock_measure

        stats.stats.view_manager.register_view(mock_view)

        mmap = stats.stats.stats_recorder.new_measurement_map()
        mmap.measure_float_put(mock_measure, 1.0)
        mmap.record()

        # Reaching into the stats internals here to check that recording the
        # measurement map affects view data.
        m2vd = (stats.stats.view_manager.measure_to_view_map
                ._measure_to_view_data_list_map)
        self.assertIn(mock_measure_name, m2vd)
        [view_data] = m2vd[mock_measure_name]
        agg_data = view_data.tag_value_aggregation_data_map[tuple()]
        agg_data.add_sample.assert_called_once()

    @mock.patch('opencensus.ext.stackdriver.stats_exporter'
                '.monitoring_v3.MetricServiceClient')
    def test_new_stats_exporter(self, mock_client):
        transport = stats_exporter.new_stats_exporter()
        self.assertIsNotNone(transport)
        self.assertIsNotNone(transport.options)
        self.assertIsNotNone(transport.options.project_id)
