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

import re

from apiclient.http import HttpMock
import main
import mock
import testing
import webtest


class TestAuthSample(testing.AppEngineTest):

    def setUp(self):
        super(TestAuthSample, self).setUp()
        self.app = webtest.TestApp(main.app)
        main.PROJECTID = self.config.GCLOUD_PROJECT

    def test_anonymous_get(self):
        response = self.app.get('/')

        # Should redirect to login
        self.assertEqual(response.status_int, 302)
        self.assertRegexpMatches(response.headers['Location'],
                                 r'.*accounts.*Login.*')

    def test_loggedin_get(self):
        self.login_user()

        response = self.app.get('/')

        # Should redirect to login
        self.assertEqual(response.status_int, 302)
        self.assertRegexpMatches(response.headers['Location'], r'.*oauth2.*')

    @mock.patch.object(main.decorator, 'has_credentials', return_value=True)
    def test_oauthed_get(self, *args):
        self.login_user()

        mock_http = HttpMock(
            self.resource_path('datasets-list.json'),
            {'status': '200'})

        with mock.patch.object(main.decorator, 'http', return_value=mock_http):
            response = self.app.get('/')

        # Should make the api call
        self.assertEqual(response.status_int, 200)
        self.assertRegexpMatches(
            response.body,
            re.compile(r'.*datasets.*datasetReference.*etag.*', re.DOTALL))
