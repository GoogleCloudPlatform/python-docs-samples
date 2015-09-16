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
#
"""Tests for load_data_from_csv."""
import os

from tests import CloudBaseTest

from .load_data_from_csv import main


class TestLoadDataFromCSV(CloudBaseTest):
    dataset_id = 'test_dataset'
    table_id = 'test_import_table'

    def test_load_table(self):
        cloud_storage_input_uri = 'gs://{}/data.csv'.format(self.bucket_name)
        schema_file = os.path.join(self.resource_path, 'schema.json')

        main(
            self.project_id,
            self.dataset_id,
            self.table_id,
            schema_file=schema_file,
            data_path=cloud_storage_input_uri,
            poll_interval=1,
            num_retries=5)
