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

from bigquery.samples.async_query import main, run
import tests


class TestAsyncQuery(tests.CloudBaseTest):

    def test_async_query(self):
        for result in run(self.constants['projectId'],
                          self.constants['query'],
                          False,
                          5,
                          5):
            self.assertIsNotNone(json.loads(result))


class TestAsyncRunner(tests.CloudBaseTest):

    def test_async_query_runner(self):
        test_project_id = os.environ.get(tests.PROJECT_ID_ENV)
        answers = [test_project_id, self.constants['query'], 'n',
                   '1', '1']

        with tests.mock_input_answers(
                answers, target='bigquery.samples.async_query.input'):
            main()
