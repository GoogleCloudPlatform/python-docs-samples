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

import re

from gcp.testing.flaky import flaky

from load_data_by_post import load_data

DATASET_ID = 'ephemeral_test_dataset'
TABLE_ID = 'load_data_by_post'


@flaky
def test_load_csv_data(cloud_config, resource, capsys):
    schema_path = resource('schema.json')
    data_path = resource('data.csv')

    load_data(
        schema_path,
        data_path,
        cloud_config.project,
        DATASET_ID,
        TABLE_ID
    )

    out, _ = capsys.readouterr()

    assert re.search(re.compile(
        r'Waiting for job to finish.*Job complete.', re.DOTALL), out)


@flaky
def test_load_json_data(cloud_config, resource, capsys):
    schema_path = resource('schema.json')
    data_path = resource('data.json')

    load_data(
        schema_path,
        data_path,
        cloud_config.project,
        DATASET_ID,
        TABLE_ID
    )

    out, _ = capsys.readouterr()

    assert re.search(re.compile(
        r'Waiting for job to finish.*Job complete.', re.DOTALL), out)
