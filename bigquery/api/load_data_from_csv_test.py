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


from load_data_from_csv import main
import pytest
from testing import CloudTest


@pytest.mark.slow
class TestLoadDataFromCSV(CloudTest):
    dataset_id = 'test_dataset'
    table_id = 'test_import_table'

    def test_load_table(self):
        cloud_storage_input_uri = 'gs://{}/data.csv'.format(
            self.config.CLOUD_STORAGE_BUCKET)
        schema_file = self.resource_path('schema.json')

        main(
            self.config.GCLOUD_PROJECT,
            self.dataset_id,
            self.table_id,
            schema_file=schema_file,
            data_path=cloud_storage_input_uri,
            poll_interval=1,
            num_retries=5)
