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

from load_data_by_post import load_data
import pytest
import testing


@pytest.mark.slow
class TestLoadDataByPost(testing.CloudTest):
    dataset_id = 'ephemeral_test_dataset'
    table_id = 'load_data_by_post'

    def test_load_csv_data(self):
        schema_path = self.resource_path('schema.json')
        data_path = self.resource_path('data.csv')
        with testing.capture_stdout() as mock_stdout:
            load_data(schema_path,
                      data_path,
                      self.config.GCLOUD_PROJECT,
                      self.dataset_id,
                      self.table_id
                      )

        stdout = mock_stdout.getvalue()

        self.assertRegexpMatches(stdout, re.compile(
            r'Waiting for job to finish.*Job complete.', re.DOTALL))

    def test_load_json_data(self):
        schema_path = self.resource_path('schema.json')
        data_path = self.resource_path('data.json')

        with testing.capture_stdout() as mock_stdout:
            load_data(schema_path,
                      data_path,
                      self.config.GCLOUD_PROJECT,
                      self.dataset_id,
                      self.table_id
                      )

        stdout = mock_stdout.getvalue()

        self.assertRegexpMatches(stdout, re.compile(
            r'Waiting for job to finish.*Job complete.', re.DOTALL))
