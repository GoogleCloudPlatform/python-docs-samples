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

from sync_query import sync_query


def test_sync_query(capsys):
    query = (
        'SELECT corpus FROM `publicdata.samples.shakespeare` '
        'GROUP BY corpus;')

    sync_query(query)

    out, _ = capsys.readouterr()

    assert 'romeoandjuliet' in out
