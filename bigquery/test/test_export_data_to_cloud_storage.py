"""Tests for export_table_to_gcs."""
from test.base_test import BaseBigqueryTest
from samples.export_data_to_cloud_storage import run
import unittest


class TestExportTableToGCS(BaseBigqueryTest):

    def test_export_table(self):
        run(self.constants['cloudStorageInputURI'],
            self.constants['projectId'],
            self.constants['datasetId'],
            self.constants['newTableId'],
            5,
            5)

if __name__ == '__main__':
    unittest.main()
