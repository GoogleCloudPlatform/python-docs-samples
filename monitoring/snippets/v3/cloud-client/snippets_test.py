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

import backoff
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import ServerError
from google.api_core.exceptions import ServiceUnavailable
import pytest

import snippets


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="function")
def custom_metric_descriptor() -> None:
    descriptor = snippets.create_metric_descriptor(PROJECT_ID)
    if descriptor is not None:
        yield descriptor.name
    else:
        yield None

    # teardown
    try:
        if descriptor is not None:
            snippets.delete_metric_descriptor(descriptor.name)
    except NotFound:
        print("Metric descriptor already deleted")


@pytest.fixture(scope="module")
def write_time_series() -> None:
    @backoff.on_exception(backoff.expo, ServerError, max_time=120)
    def write():
        snippets.write_time_series(PROJECT_ID)

    try:
        write()
    except ServerError:
        #
        pytest.skip(
            "Failed to prepare test fixture due to Internal server error. Not our fault 🤷"
        )

    yield


def test_get_delete_metric_descriptor(custom_metric_descriptor) -> None:
    try:

        @backoff.on_exception(backoff.expo, (AssertionError, NotFound), max_time=60)
        def eventually_consistent_test():
            result = snippets.get_metric_descriptor(custom_metric_descriptor)
            assert result.value_type == 3  # (3 == MetricDescriptor.ValueType.DOUBLE)

        eventually_consistent_test()
    finally:
        snippets.delete_metric_descriptor(custom_metric_descriptor)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_metric_descriptors() -> None:
    result = snippets.list_metric_descriptors(PROJECT_ID)
    results = [item.type for item in result]
    assert "logging.googleapis.com/byte_count" in results


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_resources() -> None:
    result = snippets.list_monitored_resources(PROJECT_ID)
    assert any(item.type == "pubsub_topic" for item in result)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_get_resources() -> None:
    result = snippets.get_monitored_resource_descriptor(PROJECT_ID, "pubsub_topic")
    assert result.display_name == "Cloud Pub/Sub Topic"


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series(write_time_series) -> None:
    result = snippets.list_time_series(PROJECT_ID)
    assert any(item.resource.type == "gce_instance" for item in result)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series_header(write_time_series) -> None:
    result = snippets.list_time_series_header(PROJECT_ID)
    assert any(item.resource.type == "gce_instance" for item in result)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series_aggregate(write_time_series) -> None:
    result = snippets.list_time_series_aggregate(PROJECT_ID)
    assert any(item.resource.type == "gce_instance" for item in result)


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series_reduce(write_time_series) -> None:
    result = snippets.list_time_series_reduce(PROJECT_ID)
    assert any(item.resource.type == "gce_instance" for item in result)
