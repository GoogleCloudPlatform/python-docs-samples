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
import json
import unittest

from bigquery.samples.async_query import run
from bigquery.test.base_test import BaseBigqueryTest


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
