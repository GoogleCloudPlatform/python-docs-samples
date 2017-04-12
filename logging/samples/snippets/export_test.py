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

import os
import random
import string

from gcp_devrel.testing import eventually_consistent
from google.cloud import logging
import pytest

import export

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
TEST_SINK_NAME_TMPL = 'example_sink_{}'
TEST_SINK_FILTER = 'severity>=CRITICAL'


def _random_id():
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(6))


@pytest.yield_fixture
def example_sink():
    client = logging.Client()

    sink = client.sink(
        TEST_SINK_NAME_TMPL.format(_random_id()),
        TEST_SINK_FILTER,
        'storage.googleapis.com/{bucket}'.format(bucket=BUCKET))

    sink.create()

    yield sink

    try:
        sink.delete()
    except:
        pass


def test_list(example_sink, capsys):
    @eventually_consistent.call
    def _():
        export.list_sinks()
        out, _ = capsys.readouterr()
        assert example_sink.name in out


def test_create(capsys):
    sink_name = TEST_SINK_NAME_TMPL.format(_random_id())

    try:
        export.create_sink(
            sink_name,
            BUCKET,
            TEST_SINK_FILTER)
    # Clean-up the temporary sink.
    finally:
        try:
            logging.Client().sink(sink_name).delete()
        except:
            pass

    out, _ = capsys.readouterr()
    assert sink_name in out


def test_update(example_sink, capsys):
    updated_filter = 'severity>=INFO'
    export.update_sink(example_sink.name, updated_filter)

    example_sink.reload()
    assert example_sink.filter_ == updated_filter


def test_delete(example_sink, capsys):
    export.delete_sink(example_sink.name)
    assert not example_sink.exists()
