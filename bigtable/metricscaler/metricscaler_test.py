# Copyright 2017 Google Inc.
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

"""Unit and system tests for metricscaler.py"""

import os
import time

from google.cloud import bigtable
from mock import patch

from metricscaler import get_cpu_load
from metricscaler import main
from metricscaler import scale_bigtable

# tests assume instance and cluster have the same ID
BIGTABLE_INSTANCE = os.environ['BIGTABLE_CLUSTER']
SIZE_CHANGE_STEP = 3

# System tests to verify API calls succeed


def test_get_cpu_load():
    assert get_cpu_load() > 0.0


def test_scale_bigtable():
    bigtable_client = bigtable.Client(admin=True)
    instance = bigtable_client.instance(BIGTABLE_INSTANCE)
    instance.reload()

    cluster = instance.cluster(BIGTABLE_INSTANCE)
    cluster.reload()
    original_node_count = cluster.serve_nodes

    scale_bigtable(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, True)

    time.sleep(3)
    cluster.reload()

    new_node_count = cluster.serve_nodes
    assert (new_node_count == (original_node_count + SIZE_CHANGE_STEP))

    scale_bigtable(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, False)
    time.sleep(3)
    cluster.reload()
    final_node_count = cluster.serve_nodes
    assert final_node_count == original_node_count


# Unit test for logic
@patch('time.sleep')
@patch('metricscaler.get_cpu_load')
@patch('metricscaler.scale_bigtable')
def test_main(scale_bigtable, get_cpu_load, sleep):
    SHORT_SLEEP = 5
    LONG_SLEEP = 10
    get_cpu_load.return_value = 0.5

    main(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, 0.6, 0.3, SHORT_SLEEP,
         LONG_SLEEP)
    scale_bigtable.assert_not_called()
    scale_bigtable.reset_mock()

    get_cpu_load.return_value = 0.7
    main(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, 0.6, 0.3, SHORT_SLEEP,
         LONG_SLEEP)
    scale_bigtable.assert_called_once_with(BIGTABLE_INSTANCE,
                                           BIGTABLE_INSTANCE, True)
    scale_bigtable.reset_mock()

    get_cpu_load.return_value = 0.2
    main(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, 0.6, 0.3, SHORT_SLEEP,
         LONG_SLEEP)
    scale_bigtable.assert_called_once_with(BIGTABLE_INSTANCE,
                                           BIGTABLE_INSTANCE, False)

    scale_bigtable.reset_mock()
