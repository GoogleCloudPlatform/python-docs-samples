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
import re

import backoff
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import ServiceUnavailable
import pytest

import snippets


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="function")
def custom_metric_descriptor(capsys):
    snippets.create_metric_descriptor(PROJECT_ID)
    out, _ = capsys.readouterr()
    match = re.search(r"Created (.*)\.", out)
    metric_name = match.group(1)
    yield metric_name

    # teardown
    try:
        snippets.delete_metric_descriptor(metric_name)
    except NotFound:
        print("Metric descriptor already deleted")


@pytest.fixture(scope="module")
def write_time_series():
    @backoff.on_exception(backoff.expo, InternalServerError, max_time=120)
    def write():
        snippets.write_time_series(PROJECT_ID)

    write()
    yield


def test_get_delete_metric_descriptor(capsys, custom_metric_descriptor):
    try:

        @backoff.on_exception(backoff.expo, (AssertionError, NotFound), max_time=60)
        def eventually_consistent_test():
            snippets.get_metric_descriptor(custom_metric_descriptor)
            out, _ = capsys.readouterr()
            assert "DOUBLE" in out

        eventually_consistent_test()
    finally:
        snippets.delete_metric_descriptor(custom_metric_descriptor)
        out, _ = capsys.readouterr()
    assert "Deleted metric" in out


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_metric_descriptors(capsys):
    snippets.list_metric_descriptors(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "logging.googleapis.com/byte_count" in out


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_resources(capsys):
    snippets.list_monitored_resources(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "pubsub_topic" in out


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_get_resources(capsys):
    snippets.get_monitored_resource_descriptor(PROJECT_ID, "pubsub_topic")
    out, _ = capsys.readouterr()
    assert "A topic in Google Cloud Pub/Sub" in out


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series(capsys, write_time_series):
    snippets.list_time_series(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "gce_instance" in out


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series_header(capsys, write_time_series):
    snippets.list_time_series_header(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "gce_instance" in out


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series_aggregate(capsys, write_time_series):
    snippets.list_time_series_aggregate(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "points" in out
    assert "interval" in out
    assert "start_time" in out
    assert "end_time" in out


@backoff.on_exception(backoff.expo, (ServiceUnavailable), max_tries=3)
def test_list_time_series_reduce(capsys, write_time_series):
    snippets.list_time_series_reduce(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "points" in out
    assert "interval" in out
    assert "start_time" in out
    assert "end_time" in out
