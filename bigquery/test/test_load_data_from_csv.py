"""Tests for load_data_from_csv."""

from test.base_test import BaseBigqueryTest
from test import RESOURCE_PATH
from samples.load_data_from_csv import run
import os
import json
import unittest


class TestLoadDataFromCSV(BaseBigqueryTest):

    def setUp(self):
        super(TestLoadDataFromCSV, self).setUp()
        with open(
                os.path.join(RESOURCE_PATH, 'schema.json'),
                'r') as schema_file:
            self.schema = json.load(schema_file)

    def test_load_table(self):
        run(self.schema,
            self.constants['cloudStorageInputURI'],
            self.constants['projectId'],
            self.constants['datasetId'],
            self.constants['newTableId'],
            5,
            5)


if __name__ == '__main__':
    unittest.main()
