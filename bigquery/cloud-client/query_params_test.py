# Copyright 2016 Google Inc.
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

import query_params


def test_query_array_params(capsys):
    query_params.query_array_params(
        gender='M',
        states=['WA', 'WI', 'WV', 'WY'])
    out, _ = capsys.readouterr()
    assert 'James' in out


def test_query_named_params(capsys):
    query_params.query_named_params(
        corpus='romeoandjuliet',
        min_word_count=100)
    out, _ = capsys.readouterr()
    assert 'the' in out


def test_query_positional_params(capsys):
    query_params.query_positional_params(
        corpus='romeoandjuliet',
        min_word_count=100)
    out, _ = capsys.readouterr()
    assert 'the' in out


def test_query_struct_params(capsys):
    query_params.query_struct_params(765, "hello world")
    out, _ = capsys.readouterr()
    assert '765' in out
    assert 'hello world' in out


def test_query_timestamp_params(capsys):
    query_params.query_timestamp_params(2016, 12, 7, 8, 0)
    out, _ = capsys.readouterr()
    assert '2016, 12, 7, 9, 0' in out
