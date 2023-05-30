# Copyright 2017 Google LLC
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

import os
import uuid
from unittest import mock

import backoff
from google.api.monitored_resource_pb2 import MonitoredResource
from google.api.monitored_resource_pb2 import MonitoredResourceDescriptor
from google.api.metric_pb2 import MetricDescriptor
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import ServiceUnavailable
from google.cloud.monitoring_v3.types import TimeSeries
import pytest

import snippets


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="function")
def mock_timeseries_list():
    resource = mock.MagicMock(spec=MonitoredResource)
    resource.type = "gce_instance"
    time_series = mock.MagicMock(spec=TimeSeries)
    time_series.resource = resource
    yield mock.MagicMock(return_value=[time_series])


@pytest.fixture(scope="function")
def mock_resource_descriptors_list():
    descriptor = mock.MagicMock(spec=MonitoredResourceDescriptor)
    descriptor.type = "pubsub_topic"
    yield mock.MagicMock(return_value=[descriptor])


@pytest.fixture(scope="function")
def mock_resource_descriptor():
    descriptor = mock.MagicMock(spec=MonitoredResourceDescriptor)
    descriptor.display_name = "Cloud Pub/Sub Topic"
    yield mock.MagicMock(return_value=descriptor)


@pytest.fixture(scope="function")
def mock_metric_descriptor():
    descriptor = mock.MagicMock(spec=MetricDescriptor)
    descriptor.name = f"projects/{PROJECT_ID}/metricsDescriptors/custom.googleapis.com/my_metric{uuid.uuid4()}"
    descriptor.value_type = 3
    yield mock.MagicMock(return_value=descriptor)


@pytest.fixture(scope="function")
def mock_metric_descriptors_list():
    descriptor = mock.MagicMock(spec=MetricDescriptor)
    descriptor.type = "logging.googleapis.com/byte_count"
    yield mock.MagicMock(return_value=[descriptor])


@pytest.fixture(scope="function")
def custom_metric_descriptor(mock_metric_descriptor) -> None:
    with mock.patch(
        "google.cloud.monitoring_v3.MetricServiceClient.create_metric_descriptor",
        mock_metric_descriptor,
    ):
        descriptor = snippets.create_metric_descriptor(PROJECT_ID)
    if descriptor is not None:
        yield descriptor.name
    else:
        yield None

    # teardown
    try:
        if descriptor is not None:
            with mock.patch(
                "google.cloud.monitoring_v3.MetricServiceClient.delete_metric_descriptor"
            ):
                snippets.delete_metric_descriptor(descriptor.name)
    except NotFound:
        print("Metric descriptor already deleted")


@pytest.fixture(scope="module")
def write_time_series() -> None:
    @backoff.on_exception(backoff.expo, InternalServerError, max_time=120)
    def write():
        snippets.write_time_series(PROJECT_ID)

    with mock.patch(
        "google.cloud.monitoring_v3.MetricServiceClient.create_time_series"
    ):
        write()
    yield


def test_get_delete_metric_descriptor(custom_metric_descriptor, mock_metric_descriptor) -> None:
    try:

        @backoff.on_exception(backoff.expo, (AssertionError, NotFound), max_time=60)
        def eventually_consistent_test():
            result = snippets.get_metric_descriptor(custom_metric_descriptor)
            assert result.value_type == 3  # (3 == MetricDescriptor.ValueType.DOUBLE)

        with mock.patch(
            "google.cloud.monitoring_v3.MetricServiceClient.get_metric_descriptor",
            mock_metric_descriptor,
        ):
            eventually_consistent_test()
    finally:
        with mock.patch(
            "google.cloud.monitoring_v3.MetricServiceClient.delete_metric_descriptor"
        ):
            snippets.delete_metric_descriptor(custom_metric_descriptor)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_metric_descriptors(mock_metric_descriptors_list) -> None:
    with mock.patch(
        "google.cloud.monitoring_v3.MetricServiceClient.list_metric_descriptors",
        mock_metric_descriptors_list,
    ):
        result = snippets.list_metric_descriptors(PROJECT_ID)
        assert any(item.type == "logging.googleapis.com/byte_count" for item in result)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_resources(mock_resource_descriptors_list) -> None:
    with mock.patch(
        "google.cloud.monitoring_v3.MetricServiceClient.list_monitored_resource_descriptors",
        mock_resource_descriptors_list,
    ):
        result = snippets.list_monitored_resources(PROJECT_ID)
        assert any(item.type == "pubsub_topic" for item in result)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_get_resources(mock_resource_descriptor) -> None:
    with mock.patch(
        "google.cloud.monitoring_v3.MetricServiceClient.get_monitored_resource_descriptor",
        mock_resource_descriptor,
    ):
        result = snippets.get_monitored_resource_descriptor(PROJECT_ID, "pubsub_topic")
        assert result.display_name == "Cloud Pub/Sub Topic"


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series(write_time_series, mock_timeseries_list) -> None:
    with mock.patch(
        "google.cloud.monitoring_v3.MetricServiceClient.list_time_series",
        mock_timeseries_list,
    ):
        result = snippets.list_time_series(PROJECT_ID)
        assert any(item.resource.type == "gce_instance" for item in result)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series_header(write_time_series, mock_timeseries_list) -> None:
    with mock.patch(
        "google.cloud.monitoring_v3.MetricServiceClient.list_time_series",
        mock_timeseries_list,
    ):
        result = snippets.list_time_series_header(PROJECT_ID)
        assert any(item.resource.type == "gce_instance" for item in result)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series_aggregate(write_time_series, mock_timeseries_list) -> None:
    with mock.patch(
        "google.cloud.monitoring_v3.MetricServiceClient.list_time_series",
        mock_timeseries_list,
    ):
        result = snippets.list_time_series_aggregate(PROJECT_ID)
        assert any(item.resource.type == "gce_instance" for item in result)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series_reduce(write_time_series, mock_timeseries_list) -> None:
    with mock.patch(
        "google.cloud.monitoring_v3.MetricServiceClient.list_time_series",
        mock_timeseries_list,
    ):
        result = snippets.list_time_series_reduce(PROJECT_ID)
        assert any(item.resource.type == "gce_instance" for item in result)
