from test.base_test import BaseBigqueryTest
from samples.async_query import run
import json
import unittest


class TestAsyncQuery(BaseBigqueryTest):

    def test_async_query(self):
        for result in run(self.constants['projectId'],
                          self.constants['query'],
                          False,
                          5,
                          5):
            self.assertIsNotNone(json.loads(result))


if __name__ == '__main__':
    unittest.main()
