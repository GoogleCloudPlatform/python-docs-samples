# Copyright 2016 Google Inc. All rights reserved.
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

import os

from google.appengine.ext import testbed as gaetestbed
import mock
import webtest

import main


def test_app(testbed):
    key_name = 'foo'

    testbed.init_taskqueue_stub(root_path=os.path.dirname(__file__))

    app = webtest.TestApp(main.app)
    app.post('/', {'key': key_name})

    tq_stub = testbed.get_stub(gaetestbed.TASKQUEUE_SERVICE_NAME)
    tasks = tq_stub.get_filtered_tasks()
    assert len(tasks) == 1
    assert tasks[0].name == 'task1'

    with mock.patch('main.update_counter') as mock_update:
        # Force update to fail, otherwise the loop will go forever.
        mock_update.side_effect = RuntimeError()

        app.get('/_ah/start', status=500)

        assert mock_update.called
