import unittest

from samples.sync_query import run
from test.base_test import BaseBigqueryTest
import json


class TestSyncQuery(BaseBigqueryTest):

    def test_sync_query(self):
        for result in run(self.constants['projectId'],
                          self.constants['query'],
                          5000,
                          5):

            self.assertIsNotNone(json.loads(result))


if __name__ == '__main__':
    unittest.main()
