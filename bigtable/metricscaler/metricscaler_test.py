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
import uuid

import pytest
from google.cloud import bigtable
from google.cloud.bigtable import enums
from mock import patch

from metricscaler import get_cpu_load
from metricscaler import get_storage_utilization
from metricscaler import main
from metricscaler import scale_bigtable

PROJECT = os.environ['GCLOUD_PROJECT']
BIGTABLE_ZONE = os.environ['BIGTABLE_ZONE']
SIZE_CHANGE_STEP = 3
INSTANCE_ID_FORMAT = 'metric-scale-test-{}'
BIGTABLE_INSTANCE = INSTANCE_ID_FORMAT.format(str(uuid.uuid4())[:10])
BIGTABLE_DEV_INSTANCE = INSTANCE_ID_FORMAT.format(str(uuid.uuid4())[:10])


# System tests to verify API calls succeed


def test_get_cpu_load():
    assert float(get_cpu_load()) > 0.0


def test_get_storage_utilization():
    assert float(get_storage_utilization()) > 0.0


@pytest.fixture()
def instance():
    cluster_id = BIGTABLE_INSTANCE

    client = bigtable.Client(project=PROJECT, admin=True)

    serve_nodes = 3
    storage_type = enums.StorageType.SSD
    production = enums.Instance.Type.PRODUCTION
    labels = {'prod-label': 'prod-label'}
    instance = client.instance(BIGTABLE_INSTANCE, instance_type=production,
                               labels=labels)

    if not instance.exists():
        cluster = instance.cluster(cluster_id, location_id=BIGTABLE_ZONE,
                                   serve_nodes=serve_nodes,
                                   default_storage_type=storage_type)
        instance.create(clusters=[cluster])

    yield

    instance.delete()


@pytest.fixture()
def dev_instance():
    cluster_id = BIGTABLE_DEV_INSTANCE

    client = bigtable.Client(project=PROJECT, admin=True)

    storage_type = enums.StorageType.SSD
    development = enums.Instance.Type.DEVELOPMENT
    labels = {'dev-label': 'dev-label'}
    instance = client.instance(BIGTABLE_DEV_INSTANCE,
                               instance_type=development,
                               labels=labels)

    if not instance.exists():
        cluster = instance.cluster(cluster_id, location_id=BIGTABLE_ZONE,
                                   default_storage_type=storage_type)
        instance.create(clusters=[cluster])

    yield

    instance.delete()


def test_scale_bigtable(instance):
    bigtable_client = bigtable.Client(admin=True)

    instance = bigtable_client.instance(BIGTABLE_INSTANCE)
    instance.reload()

    cluster = instance.cluster(BIGTABLE_INSTANCE)
    cluster.reload()
    original_node_count = cluster.serve_nodes

    scale_bigtable(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, True)

    for n in range(10):
        time.sleep(10)
        cluster.reload()
        new_node_count = cluster.serve_nodes
        try:
            assert (new_node_count == (original_node_count + SIZE_CHANGE_STEP))
        except AssertionError:
            if n == 9:
                raise

    scale_bigtable(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, False)

    for n in range(10):
        time.sleep(10)
        cluster.reload()
        final_node_count = cluster.serve_nodes
        try:
            assert final_node_count == original_node_count
        except AssertionError:
            if n == 9:
                raise


def test_handle_dev_instance(capsys, dev_instance):
    with pytest.raises(ValueError):
        scale_bigtable(BIGTABLE_DEV_INSTANCE, BIGTABLE_DEV_INSTANCE, True)


@patch('time.sleep')
@patch('metricscaler.get_storage_utilization')
@patch('metricscaler.get_cpu_load')
@patch('metricscaler.scale_bigtable')
def test_main(scale_bigtable, get_cpu_load, get_storage_utilization, sleep):
    SHORT_SLEEP = 5
    LONG_SLEEP = 10

    # Test okay CPU, okay storage utilization
    get_cpu_load.return_value = 0.5
    get_storage_utilization.return_value = 0.5

    main(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, 0.6, 0.3, 0.6, SHORT_SLEEP,
         LONG_SLEEP)
    scale_bigtable.assert_not_called()
    scale_bigtable.reset_mock()

    # Test high CPU, okay storage utilization
    get_cpu_load.return_value = 0.7
    get_storage_utilization.return_value = 0.5
    main(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, 0.6, 0.3, 0.6, SHORT_SLEEP,
         LONG_SLEEP)
    scale_bigtable.assert_called_once_with(BIGTABLE_INSTANCE,
                                           BIGTABLE_INSTANCE, True)
    scale_bigtable.reset_mock()

    # Test low CPU, okay storage utilization
    get_storage_utilization.return_value = 0.5
    get_cpu_load.return_value = 0.2
    main(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, 0.6, 0.3, 0.6, SHORT_SLEEP,
         LONG_SLEEP)
    scale_bigtable.assert_called_once_with(BIGTABLE_INSTANCE,
                                           BIGTABLE_INSTANCE, False)
    scale_bigtable.reset_mock()

    # Test okay CPU, high storage utilization
    get_cpu_load.return_value = 0.5
    get_storage_utilization.return_value = 0.7

    main(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, 0.6, 0.3, 0.6, SHORT_SLEEP,
         LONG_SLEEP)
    scale_bigtable.assert_called_once_with(BIGTABLE_INSTANCE,
                                           BIGTABLE_INSTANCE, True)
    scale_bigtable.reset_mock()

    # Test high CPU, high storage utilization
    get_cpu_load.return_value = 0.7
    get_storage_utilization.return_value = 0.7
    main(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, 0.6, 0.3, 0.6, SHORT_SLEEP,
         LONG_SLEEP)
    scale_bigtable.assert_called_once_with(BIGTABLE_INSTANCE,
                                           BIGTABLE_INSTANCE, True)
    scale_bigtable.reset_mock()

    # Test low CPU, high storage utilization
    get_cpu_load.return_value = 0.2
    get_storage_utilization.return_value = 0.7
    main(BIGTABLE_INSTANCE, BIGTABLE_INSTANCE, 0.6, 0.3, 0.6, SHORT_SLEEP,
         LONG_SLEEP)
    scale_bigtable.assert_called_once_with(BIGTABLE_INSTANCE,
                                           BIGTABLE_INSTANCE, True)
    scale_bigtable.reset_mock()
