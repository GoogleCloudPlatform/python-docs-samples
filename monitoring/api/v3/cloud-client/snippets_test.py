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

import re
import pytest
import uuid
import os

from gcp_devrel.testing import eventually_consistent

import google.api_core.exceptions
import snippets

from google.cloud import monitoring_v3

PROJECT_ID = os.environ["GCLOUD_PROJECT"]


@pytest.fixture(scope="module")
def test_custom_metric_descriptor():
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(PROJECT_ID)
    descriptor = monitoring_v3.types.MetricDescriptor()
    descriptor.type = "custom.googleapis.com/my_metric" + str(uuid.uuid4())
    descriptor.metric_kind = monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE
    descriptor.value_type = monitoring_v3.enums.MetricDescriptor.ValueType.DOUBLE
    descriptor.description = "This is a simple example of a custom metric."
    descriptor_response = client.create_metric_descriptor(project_name, descriptor)
    yield descriptor_response.name
    try:
        snippets.delete_metric_descriptor(descriptor_response.name)
    except google.api_core.exceptions.NotFound:
        print("Metric already deleted")


def test_create_metric_descriptor(capsys):
    snippets.create_metric_descriptor(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "Created" in out
    assert "custom.googleapis.com/my_metric" in out
    # cleanup from test
    match = re.search(r"Created (.*)\.", out)
    metric_name = match.group(1)
    snippets.delete_metric_descriptor(metric_name)


def test_get_metric_descriptor(test_custom_metric_descriptor, capsys):
    try:

        @eventually_consistent.call
        def __():
            snippets.get_metric_descriptor(test_custom_metric_descriptor)

        out, _ = capsys.readouterr()
        assert test_custom_metric_descriptor in out
    except Exception as e:
        print(e)


def test_delete_metric_descriptor(test_custom_metric_descriptor, capsys):
    snippets.delete_metric_descriptor(test_custom_metric_descriptor)
    out, _ = capsys.readouterr()
    assert "Deleted metric" in out
    assert test_custom_metric_descriptor in out


def test_list_metric_descriptors(capsys):
    snippets.list_metric_descriptors(snippets.project_id())
    out, _ = capsys.readouterr()
    assert "logging.googleapis.com/byte_count" in out


def test_list_resources(capsys):
    snippets.list_monitored_resources(snippets.project_id())
    out, _ = capsys.readouterr()
    assert "pubsub_topic" in out


def test_get_resources(capsys):
    snippets.get_monitored_resource_descriptor(snippets.project_id(), "pubsub_topic")
    out, _ = capsys.readouterr()
    assert "A topic in Google Cloud Pub/Sub" in out


def test_write_time_series(capsys):
    snippets.write_time_series(snippets.project_id())
    out, _ = capsys.readouterr()
    assert "Error" not in out  # this method returns nothing unless there is an error
    # clean up custom metric created as part of quickstart
    match = re.search(r"Metric to clean up (.*)\.", out)
    metric_name = "projects/{}/metricDescriptors/{}".format(PROJECT_ID, match.group(1))
    snippets.delete_metric_descriptor(metric_name)


def test_list_time_series(capsys):
    snippets.list_time_series(snippets.project_id())
    out, _ = capsys.readouterr()
    assert "gce_instance" in out


def test_list_time_series_header(capsys):
    snippets.list_time_series_header(snippets.project_id())
    out, _ = capsys.readouterr()
    assert "gce_instance" in out


def test_list_time_series_aggregate(capsys):
    snippets.list_time_series_aggregate(snippets.project_id())
    out, _ = capsys.readouterr()
    assert "points" in out
    assert "interval" in out
    assert "start_time" in out
    assert "end_time" in out


def test_list_time_series_reduce(capsys):
    snippets.list_time_series_reduce(snippets.project_id())
    out, _ = capsys.readouterr()
    assert "points" in out
    assert "interval" in out
    assert "start_time" in out
    assert "end_time" in out
