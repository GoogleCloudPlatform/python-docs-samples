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

""" Integration test for list_env.py

GOOGLE_APPLICATION_CREDENTIALS must be set to a Service Account for a project
that has enabled the Monitoring API.

Currently the TEST_PROJECT_ID is hard-coded to run using the project created
for this test, but it could be changed to a different project.
"""

import os
import re

from gcp_devrel.testing.flaky import flaky
import googleapiclient.discovery
import pytest

import list_resources

PROJECT = os.environ['GCLOUD_PROJECT']
METRIC = 'compute.googleapis.com/instance/cpu/usage_time'


@pytest.fixture(scope='module')
def client():
    return googleapiclient.discovery.build('monitoring', 'v3')


@flaky
def test_list_monitored_resources(client, capsys):
    PROJECT_RESOURCE = "projects/{}".format(PROJECT)
    list_resources.list_monitored_resource_descriptors(
        client, PROJECT_RESOURCE)
    stdout, _ = capsys.readouterr()
    regex = re.compile(
        'An application running', re.I)
    assert regex.search(stdout) is not None


@flaky
def test_list_metrics(client, capsys):
    PROJECT_RESOURCE = "projects/{}".format(PROJECT)
    list_resources.list_metric_descriptors(
        client, PROJECT_RESOURCE, METRIC)
    stdout, _ = capsys.readouterr()
    regex = re.compile(
        u'Delta CPU', re.I)
    assert regex.search(stdout) is not None


@flaky
def test_list_timeseries(client, capsys):
    PROJECT_RESOURCE = "projects/{}".format(PROJECT)
    list_resources.list_timeseries(
        client, PROJECT_RESOURCE, METRIC)
    stdout, _ = capsys.readouterr()
    regex = re.compile(u'list_timeseries response:\n', re.I)
    assert regex.search(stdout) is not None
