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
import os

from sync_query import main

PROJECT = os.environ['GCLOUD_PROJECT']


def test_sync_query(capsys):
    query = (
        'SELECT corpus FROM publicdata:samples.shakespeare '
        'GROUP BY corpus;')

    main(
        project_id=PROJECT,
        query=query,
        timeout=30,
        num_retries=5,
        use_legacy_sql=True)

    out, _ = capsys.readouterr()
    result = out.split('\n')[0]

    assert json.loads(result) is not None


def test_sync_query_standard_sql(capsys):
    query = 'SELECT [1, 2, 3] AS arr;'  # Only valid in standard SQL

    main(
        project_id=PROJECT,
        query=query,
        timeout=30,
        num_retries=5,
        use_legacy_sql=False)

    out, _ = capsys.readouterr()
    result = out.split('\n')[0]

    assert json.loads(result) is not None
