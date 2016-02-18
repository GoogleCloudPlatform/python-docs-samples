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
from testing import capture_stdout, CloudTest


class TestStreaming(CloudTest):
    dataset_id = 'test_dataset'
    table_id = 'test_table'

    def test_stream_row_to_bigquery(self):
        with open(
                self.resource_path('streamrows.json'),
                'r') as rows_file:

            rows = json.load(rows_file)

        streaming.get_rows = lambda: rows

        with capture_stdout() as stdout:
            streaming.main(
                self.config.GCLOUD_PROJECT,
                self.dataset_id,
                self.table_id,
                num_retries=5)

        results = stdout.getvalue().split('\n')
        self.assertIsNotNone(json.loads(results[0]))
