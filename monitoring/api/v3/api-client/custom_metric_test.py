#!/usr/bin/env python
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


""" Integration test for custom_metric.py

GOOGLE_APPLICATION_CREDENTIALS must be set to a Service Account for a project
that has enabled the Monitoring API.

Currently the TEST_PROJECT_ID is hard-coded to run using the project created
for this test, but it could be changed to a different project.
"""

import os
import random
import time
import uuid

import backoff
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import pytest

from custom_metric import create_custom_metric
from custom_metric import delete_metric_descriptor
from custom_metric import get_custom_metric
from custom_metric import read_timeseries
from custom_metric import write_timeseries_value


PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']
PROJECT_RESOURCE = f"projects/{PROJECT}"

""" Custom metric domain for all custom metrics"""
CUSTOM_METRIC_DOMAIN = "custom.googleapis.com"

METRIC = 'compute.googleapis.com/instance/cpu/usage_time'
METRIC_NAME = uuid.uuid4().hex
METRIC_RESOURCE = "{}/{}".format(
    CUSTOM_METRIC_DOMAIN, METRIC_NAME)
METRIC_KIND = "GAUGE"


@pytest.fixture(scope='module')
def client():
    return googleapiclient.discovery.build('monitoring', 'v3')


@pytest.fixture(scope='module')
def custom_metric(client):
    custom_metric_descriptor = create_custom_metric(
        client, PROJECT_RESOURCE, METRIC_RESOURCE, METRIC_KIND)

    # Wait up to 50 seconds until metric has been created. Use the get call
    # to wait until a response comes back with the new metric with 10 retries.
    custom_metric = None
    retry_count = 0
    while not custom_metric and retry_count < 10:
        time.sleep(5)
        retry_count += 1
        custom_metric = get_custom_metric(
            client, PROJECT_RESOURCE, METRIC_RESOURCE)

    # make sure we get the custom_metric
    assert custom_metric

    yield custom_metric

    # cleanup
    delete_metric_descriptor(client, custom_metric_descriptor['name'])


def test_custom_metric(client, custom_metric):
    # Use a constant seed so psuedo random number is known ahead of time
    random.seed(1)
    pseudo_random_value = random.randint(0, 10)

    INSTANCE_ID = "test_instance"

    # It's rare, but write can fail with HttpError 500, so we retry.
    @backoff.on_exception(backoff.expo, HttpError, max_time=120)
    def write_value():
        # Reseed it to make sure the sample code will pick the same
        # value.
        random.seed(1)
        write_timeseries_value(client, PROJECT_RESOURCE,
                               METRIC_RESOURCE, INSTANCE_ID,
                               METRIC_KIND)
    write_value()

    # Sometimes on new metric descriptors, writes have a delay in being
    # read back. Use backoff to account for this.
    @backoff.on_exception(
        backoff.expo, (AssertionError, HttpError), max_time=120)
    def eventually_consistent_test():
        response = read_timeseries(
            client, PROJECT_RESOURCE, METRIC_RESOURCE)
        # Make sure the value is not empty.
        assert 'timeSeries' in response
        value = int(
            response['timeSeries'][0]['points'][0]['value']['int64Value'])
        # using seed of 1 will create a value of 1
        assert pseudo_random_value == value

    eventually_consistent_test()
