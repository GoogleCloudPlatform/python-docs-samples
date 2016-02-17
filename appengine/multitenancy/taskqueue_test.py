# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import taskqueue
import testing
import webtest


class TestNamespaceTaskQueueSample(testing.AppEngineTest):

    def setUp(self):
        super(TestNamespaceTaskQueueSample, self).setUp()
        self.app = webtest.TestApp(taskqueue.app)

    def test_get(self):
        response = self.app.get('/taskqueue')
        self.assertEqual(response.status_int, 200)
        self.assertTrue('Global: 0' in response.body)

        self.run_tasks()

        response = self.app.get('/taskqueue')
        self.assertEqual(response.status_int, 200)
        self.assertTrue('Global: 1' in response.body)

        response = self.app.get('/taskqueue/a')
        self.assertEqual(response.status_int, 200)
        self.assertTrue('a: 0' in response.body)

        self.run_tasks()

        response = self.app.get('/taskqueue/a')
        self.assertEqual(response.status_int, 200)
        self.assertTrue('a: 1' in response.body)
