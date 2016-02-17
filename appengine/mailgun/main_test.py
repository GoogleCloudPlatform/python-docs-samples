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

import main
from testing import AppEngineTest, Http2Mock
import webtest


class TestMailgunHandlers(AppEngineTest):
    def setUp(self):
        super(TestMailgunHandlers, self).setUp()

        self.app = webtest.TestApp(main.app)

    def test_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_int, 200)

    def test_post(self):
        http = Http2Mock(responses=[{}])

        with http:
            response = self.app.post('/', {
                'recipient': 'jonwayne@google.com',
                'submit': 'Send simple email'})

            self.assertEqual(response.status_int, 200)

        http = Http2Mock(responses=[{}])

        with http:
            response = self.app.post('/', {
                'recipient': 'jonwayne@google.com',
                'submit': 'Send complex email'})

            self.assertEqual(response.status_int, 200)

        http = Http2Mock(responses=[{'status': 500, 'body': 'Test error'}])

        with http, self.assertRaises(Exception):
            self.app.post('/', {
                'recipient': 'jonwayne@google.com',
                'submit': 'Send simple email'})
