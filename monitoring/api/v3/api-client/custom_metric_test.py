#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Integration test for custom_metric.py

GOOGLE_APPLICATION_CREDENTIALS must be set to a Service Account for a project
that has enabled the Monitoring API.

Currently the TEST_PROJECT_ID is hard-coded to run using the project created
for this test, but it could be changed to a different project.
"""

import os
import random
import time

from gcp.testing import eventually_consistent
from gcp.testing.flaky import flaky
import googleapiclient.discovery
import pytest

from custom_metric import create_custom_metric
from custom_metric import delete_metric_descriptor
from custom_metric import get_custom_metric
from custom_metric import read_timeseries
from custom_metric import write_timeseries_value

PROJECT = os.environ['GCLOUD_PROJECT']

""" Custom metric domain for all custom metrics"""
CUSTOM_METRIC_DOMAIN = "custom.googleapis.com"

METRIC = 'compute.googleapis.com/instance/cpu/usage_time'
METRIC_NAME = ''.join(
    random.choice('0123456789ABCDEF') for i in range(16))
METRIC_RESOURCE = "{}/{}".format(
    CUSTOM_METRIC_DOMAIN, METRIC_NAME)


@pytest.fixture(scope='module')
def client():
    return googleapiclient.discovery.build('monitoring', 'v3')


@flaky
def test_custom_metric(client):
    PROJECT_RESOURCE = "projects/{}".format(PROJECT)
    # Use a constant seed so psuedo random number is known ahead of time
    random.seed(1)
    pseudo_random_value = random.randint(0, 10)
    # Reseed it
    random.seed(1)

    INSTANCE_ID = "test_instance"
    METRIC_KIND = "GAUGE"

    custom_metric_descriptor = create_custom_metric(
        client, PROJECT_RESOURCE, METRIC_RESOURCE, METRIC_KIND)

    # wait until metric has been created, use the get call to wait until
    # a response comes back with the new metric
    custom_metric = None
    while not custom_metric:
        time.sleep(1)
        custom_metric = get_custom_metric(
            client, PROJECT_RESOURCE, METRIC_RESOURCE)

    write_timeseries_value(client, PROJECT_RESOURCE,
                           METRIC_RESOURCE, INSTANCE_ID,
                           METRIC_KIND)

    # Sometimes on new metric descriptors, writes have a delay in being
    # read back. Use eventually_consistent to account for this.
    @eventually_consistent.call
    def _():
        response = read_timeseries(client, PROJECT_RESOURCE, METRIC_RESOURCE)
        value = int(
            response['timeSeries'][0]['points'][0]['value']['int64Value'])
        # using seed of 1 will create a value of 1
        assert value == pseudo_random_value

    delete_metric_descriptor(client, custom_metric_descriptor['name'])
