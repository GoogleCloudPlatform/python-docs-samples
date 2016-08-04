# Copyright 2016 Google Inc. All Rights Reserved.
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

import export
from gcloud import logging
from gcp.testing import eventually_consistent
import pytest

TEST_SINK_NAME = 'example_sink'
TEST_SINK_FILTER = 'severity>=CRITICAL'


@pytest.fixture
def example_sink(cloud_config):
    client = logging.Client()

    sink = client.sink(
        TEST_SINK_NAME,
        TEST_SINK_FILTER,
        'storage.googleapis.com/{bucket}'.format(
            bucket=cloud_config.storage_bucket))

    if sink.exists():
        sink.delete()

    sink.create()

    return sink


def test_list(example_sink, capsys):
    @eventually_consistent.call
    def _():
        export.list_sinks()
        out, _ = capsys.readouterr()
        assert example_sink.name in out


def test_create(cloud_config, capsys):
    # Delete the sink if it exists, otherwise the test will fail in conflit.
    client = logging.Client()
    sink = client.sink(TEST_SINK_NAME)
    if sink.exists():
        sink.delete()

    export.create_sink(
        TEST_SINK_NAME,
        TEST_SINK_FILTER,
        'storage.googleapis.com/{bucket}'.format(
            bucket=cloud_config.storage_bucket))

    out, _ = capsys.readouterr()
    assert TEST_SINK_NAME in out
    assert sink.exists()


def test_update(example_sink, capsys):
    updated_filter = 'severity>=INFO'
    export.update_sink(TEST_SINK_NAME, updated_filter)

    example_sink.reload()
    assert example_sink.filter_ == updated_filter


def test_delete(example_sink, capsys):
    export.delete_sink(TEST_SINK_NAME)
    assert not example_sink.exists()
