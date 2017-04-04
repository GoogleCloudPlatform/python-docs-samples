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

import sync_query_params


def test_sync_query_named_params(capsys):
    sync_query_params.sync_query_named_params(
        corpus='romeoandjuliet',
        min_word_count=100)
    out, _ = capsys.readouterr()
    assert 'love' in out


def test_sync_query_positional_params(capsys):
    sync_query_params.sync_query_positional_params(
        corpus='romeoandjuliet',
        min_word_count=100)
    out, _ = capsys.readouterr()
    assert 'love' in out
