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

"""Tests for export_table_to_gcs."""

import unittest

from bigquery.samples.export_data_to_cloud_storage import run
from tests import CloudBaseTest


class TestExportTableToGCS(CloudBaseTest):

    def test_export_table_csv(self):
        run(self.constants['cloudStorageInputURI'],
            self.constants['projectId'],
            self.constants['datasetId'],
            self.constants['newTableId'],
            5,
            5,
            export_format="CSV")

    def test_export_table_json(self):
        run(self.constants['cloudStorageInputURI'],
            self.constants['projectId'],
            self.constants['datasetId'],
            self.constants['newTableId'],
            5,
            5,
            export_format="NEWLINE_DELIMITED_JSON")

    def test_export_table_avro(self):
        run(self.constants['cloudStorageInputURI'],
            self.constants['projectId'],
            self.constants['datasetId'],
            self.constants['newTableId'],
            5,
            5,
            export_format="AVRO")

if __name__ == '__main__':
    unittest.main()
