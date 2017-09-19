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

import query


DATASET_ID = 'test_dataset'
TABLE_ID = 'test_destination_table'


def test_query(capsys):
    # Query only outputs the first 10 rows, sort results to avoid randomness
    query_string = '''#standardSQL
          SELECT corpus
          FROM `publicdata.samples.shakespeare`
          GROUP BY corpus
          ORDER BY corpus
          LIMIT 10;'''

    query.query(query_string)

    out, _ = capsys.readouterr()

    assert 'antonyandcleopatra' in out


def test_query_standard_sql(capsys):
    # Query only outputs the first 10 rows, sort results to avoid randomness
    query_string = '''SELECT corpus
          FROM `publicdata.samples.shakespeare`
          GROUP BY corpus
          ORDER BY corpus
          LIMIT 10;'''

    query.query_standard_sql(query_string)

    out, _ = capsys.readouterr()

    assert 'antonyandcleopatra' in out


def test_query_destination_table(capsys):
    # Query only outputs the first 10 rows, sort results to avoid randomness
    query_string = '''#standardSQL
          SELECT corpus
          FROM `publicdata.samples.shakespeare`
          GROUP BY corpus
          ORDER BY corpus
          LIMIT 10;'''

    query.query_destination_table(query_string, DATASET_ID, TABLE_ID)

    out, _ = capsys.readouterr()

    assert 'antonyandcleopatra' in out
