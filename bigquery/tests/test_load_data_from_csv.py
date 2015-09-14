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

from bigquery.samples.load_data_from_csv import main
from tests import CloudBaseTest


class TestLoadDataFromCSV(CloudBaseTest):
    def test_load_table(self):
        main(
            self.constants['projectId'],
            self.constants['datasetId'],
            self.constants['newTableId'],
            os.path.join(self.resource_path, 'schema.json'),
            self.constants['cloudStorageInputURI'],
            1,
            5)
