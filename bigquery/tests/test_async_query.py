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
import os
import unittest

from bigquery.samples.async_query import run, main
from tests import CloudBaseTest, BUCKET_NAME_ENV, PROJECT_ID_ENV
from mock import patch


class TestAsyncQuery(CloudBaseTest):

    def test_async_query(self):
        for result in run(self.constants['projectId'],
                          self.constants['query'],
                          False,
                          5,
                          5):
            self.assertIsNotNone(json.loads(result))


class TestAsyncRunner(CloudBaseTest):

    i = 0

    def mock_get_input(input):
        test_bucket_name = os.environ.get(BUCKET_NAME_ENV)
        test_project_id = os.environ.get(PROJECT_ID_ENV)
        answers = [test_bucket_name, test_project_id, 'n',
                   '1', '1']
        ret = answers[TestAsyncRunner.i]
        TestAsyncRunner.i += 1
        return ret


    @patch('bigquery.samples.async_query.get_input', new=mock_get_input)
    def test_async_query_runner(self):
        main()


if __name__ == '__main__':
    unittest.main()
