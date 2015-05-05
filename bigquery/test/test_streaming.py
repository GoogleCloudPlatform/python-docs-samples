"""Tests for export_table_to_gcs."""
from samples.streaming import run
from test.base_test import BaseBigqueryTest
from test import RESOURCE_PATH
import json
import os
import unittest


class TestStreaming(BaseBigqueryTest):

    def test_stream_row_to_bigquery(self):

        with open(
                os.path.join(RESOURCE_PATH, 'streamrows.json'),
                'r') as rows_file:

            rows = json.load(rows_file)

        for result in run(self.constants['projectId'],
                          self.constants['datasetId'],
                          self.constants['newTableId'],
                          rows,
                          5):
            self.assertIsNotNone(json.loads(result))


if __name__ == '__main__':
    unittest.main()
