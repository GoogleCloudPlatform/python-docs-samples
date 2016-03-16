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

import re

import list_resources

# temporarily hard code to whitelisted project
TEST_PROJECT_ID = 'cloud-monitoring-dev'
# TEST_PROJECT_ID = os.getenv("GCLOUD_PROJECT", 'cloud-monitoring-dev')
PROJECT_RESOURCE = "projects/{}".format(TEST_PROJECT_ID)
METRIC = 'compute.googleapis.com/instance/cpu/usage_time'


def test_list_monitored_resources(capsys):
    client = list_resources.get_client()
    list_resources.list_monitored_resource_descriptors(
        client, PROJECT_RESOURCE)
    stdout, _ = capsys.readouterr()
    regex = re.compile(
        'An application running')
    assert regex.search(stdout) is not None


def test_list_metrics(capsys):
    client = list_resources.get_client()
    list_resources.list_metric_descriptors(
        client, PROJECT_RESOURCE, METRIC)
    stdout, _ = capsys.readouterr()
    regex = re.compile(
        u'Delta CPU usage time')
    assert regex.search(stdout) is not None


def test_list_timeseries(capsys):
    client = list_resources.get_client()
    list_resources.list_timeseries(
        client, PROJECT_RESOURCE, METRIC)
    stdout, _ = capsys.readouterr()
    regex = re.compile(u'list_timeseries response:\n')
    assert regex.search(stdout) is not None
