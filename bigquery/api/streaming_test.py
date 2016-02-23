# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import streaming


DATASET_ID = 'test_dataset'
TABLE_ID = 'test_table'


def test_stream_row_to_bigquery(cloud_config, resource, capsys):
    with open(resource('streamrows.json'), 'r') as rows_file:
        rows = json.load(rows_file)

    streaming.get_rows = lambda: rows

    streaming.main(
        cloud_config.project,
        DATASET_ID,
        TABLE_ID,
        num_retries=5)

    out, _ = capsys.readouterr()
    results = out.split('\n')

    assert json.loads(results[0]) is not None
