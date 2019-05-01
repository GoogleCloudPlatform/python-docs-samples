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

from gcp_devrel.testing import eventually_consistent

import snippets


def test_create_get_delete_metric_descriptor(capsys):
    snippets.create_metric_descriptor(snippets.project_id())
    out, _ = capsys.readouterr()
    match = re.search(r'Created (.*)\.', out)
    metric_name = match.group(1)
    try:
        @eventually_consistent.call
        def __():
            snippets.get_metric_descriptor(metric_name)

        out, _ = capsys.readouterr()
        assert 'DOUBLE' in out
    finally:
        snippets.delete_metric_descriptor(metric_name)
        out, _ = capsys.readouterr()
    assert 'Deleted metric' in out


def test_list_metric_descriptors(capsys):
    snippets.list_metric_descriptors(snippets.project_id())
    out, _ = capsys.readouterr()
    assert 'logging.googleapis.com/byte_count' in out


def test_list_resources(capsys):
    snippets.list_monitored_resources(snippets.project_id())
    out, _ = capsys.readouterr()
    assert 'pubsub_topic' in out


def test_get_resources(capsys):
    snippets.get_monitored_resource_descriptor(
        snippets.project_id(), 'pubsub_topic')
    out, _ = capsys.readouterr()
    assert 'A topic in Google Cloud Pub/Sub' in out


def test_time_series(capsys):
    snippets.write_time_series(snippets.project_id())

    snippets.list_time_series(snippets.project_id())
    out, _ = capsys.readouterr()
    assert 'gce_instance' in out

    snippets.list_time_series_header(snippets.project_id())
    out, _ = capsys.readouterr()
    assert 'gce_instance' in out

    snippets.list_time_series_aggregate(snippets.project_id())
    out, _ = capsys.readouterr()
    assert 'points' in out
    assert 'interval' in out
    assert 'start_time' in out
    assert 'end_time' in out

    snippets.list_time_series_reduce(snippets.project_id())
    out, _ = capsys.readouterr()
    assert 'points' in out
    assert 'interval' in out
    assert 'start_time' in out
    assert 'end_time' in out
