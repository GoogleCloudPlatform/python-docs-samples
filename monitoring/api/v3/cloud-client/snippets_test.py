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

import snippets


def test_create_and_delete_metric_descriptor(capsys):
    snippets.create_metric_descriptor()
    snippets.delete_metric_descriptor('custom.googleapis.com/my_metric')
    out, _ = capsys.readouterr()
    assert 'Deleted metric' in out


def test_list_metric_descriptors(capsys):
    snippets.list_metric_descriptors()
    out, _ = capsys.readouterr()
    assert 'logging.googleapis.com/byte_count' in out


def test_list_resources(capsys, client):
    snippets.list_monitored_resources(client)
    out, _ = capsys.readouterr()
    assert 'pubsub_topic' in out


def test_get_resource(capsys, client):
    snippets.get_monitored_resource_descriptor(client, 'pubsub_topic')
    out, _ = capsys.readouterr()
    assert 'A topic in Google Cloud Pub/Sub' in out


def test_time_series(capsys, client):
    snippets.write_time_series(client)

    snippets.list_time_series(client)
    out, _ = capsys.readouterr()
    assert 'TimeSeries with' in out

    snippets.list_time_series_header(client)
    out, _ = capsys.readouterr()
    assert 'TimeSeries with' in out

    snippets.list_time_series_aggregate(client)
    out, _ = capsys.readouterr()
    assert 'TimeSeries with' in out

    snippets.list_time_series_reduce(client)
    out, _ = capsys.readouterr()
    assert 'TimeSeries with' in out
