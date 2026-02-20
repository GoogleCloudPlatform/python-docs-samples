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
import re
import random
import string
import time

import backoff
from google.cloud import logging, storage
import pytest

import export


BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]
TEST_SINK_NAME_TMPL = "example_sink_{}_{}"
TEST_SINK_FILTER = "severity>=CRITICAL"
TIMESTAMP = int(time.time())

# Threshold beyond which the cleanup_old_sinks fixture will delete
# old sink, in seconds
CLEANUP_THRESHOLD = 7200  # 2 hours

# Max buckets to delete at a time, to mitigate operation timeout
# issues. To turn off in the future, set to None.
MAX_BUCKETS = 1500


def _random_id():
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
    )


def _create_sink_name():
    return TEST_SINK_NAME_TMPL.format(TIMESTAMP, _random_id())


@backoff.on_exception(backoff.expo, Exception, max_time=60, raise_on_giveup=False)
def _delete_object(obj, **kwargs):
    obj.delete(**kwargs)


# Runs once for entire test suite
@pytest.fixture(scope="module")
def cleanup_old_sinks():
    client = logging.Client()
    test_sink_name_regex = (
        r"^" + TEST_SINK_NAME_TMPL.format(r"(\d+)", r"[A-Z0-9]{6}") + r"$"
    )
    for sink in client.list_sinks():
        match = re.match(test_sink_name_regex, sink.name)
        if match:
            sink_timestamp = int(match.group(1))
            if TIMESTAMP - sink_timestamp > CLEANUP_THRESHOLD:
                _delete_object(sink)

    storage_client = storage.Client()

    # See _sink_storage_setup in usage_guide.py for details about how
    # sinks are named.
    test_bucket_name_regex = r"^sink\-storage\-(\d+)$"
    for bucket in storage_client.list_buckets(max_results=MAX_BUCKETS):
        match = re.match(test_bucket_name_regex, bucket.name)
        if match:
            # Bucket timestamp is int(time.time() * 1000)
            bucket_timestamp = int(match.group(1))
            if TIMESTAMP - bucket_timestamp // 1000 > CLEANUP_THRESHOLD:
                _delete_object(bucket, force=True)


@pytest.fixture
def example_sink(cleanup_old_sinks):
    client = logging.Client()

    sink = client.sink(
        _create_sink_name(),
        filter_=TEST_SINK_FILTER,
        destination="storage.googleapis.com/{bucket}".format(bucket=BUCKET),
    )

    sink.create()

    yield sink

    _delete_object(sink)


def test_list(example_sink, capsys):
    @backoff.on_exception(backoff.expo, AssertionError, max_time=60)
    def eventually_consistent_test():
        export.list_sinks()
        out, _ = capsys.readouterr()
        assert example_sink.name in out

    eventually_consistent_test()


def test_create(capsys):
    sink_name = _create_sink_name()

    try:
        export.create_sink(sink_name, BUCKET, TEST_SINK_FILTER)
    # Clean-up the temporary sink.
    finally:
        _delete_object(logging.Client().sink(sink_name))

    out, _ = capsys.readouterr()
    assert sink_name in out


def test_update(example_sink, capsys):
    updated_filter = "severity>=INFO"
    export.update_sink(example_sink.name, updated_filter)

    example_sink.reload()
    assert example_sink.filter_ == updated_filter


def test_delete(example_sink, capsys):
    export.delete_sink(example_sink.name)
    assert not example_sink.exists()
