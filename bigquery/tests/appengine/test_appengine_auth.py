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

import os
import re

from apiclient.http import HttpMock

from bigquery.samples.appengine_auth import main

import mock

import tests

import webapp2


RESOURCE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '..', 'resources')


class TestAuthSample(tests.DatastoreTestbedCase, tests.CloudBaseTest):

    def setUp(self):
        tests.DatastoreTestbedCase.setUp(self)
        tests.CloudBaseTest.setUp(self)

        self.testbed.init_user_stub()

    def loginUser(self, email='user@example.com', id='123', is_admin=False):
        self.testbed.setup_env(
            user_email=email,
            user_id=id,
            user_is_admin='1' if is_admin else '0',
            overwrite=True)

    def test_anonymous_get(self):
        request = webapp2.Request.blank('/')
        response = request.get_response(main.app)

        # Should redirect to login
        self.assertEqual(response.status_int, 302)
        self.assertRegexpMatches(response.headers['Location'],
                                 r'.*accounts.*Login.*')

    def test_loggedin_get(self):
        self.loginUser()

        request = webapp2.Request.blank('/')
        response = request.get_response(main.app)

        # Should redirect to login
        self.assertEqual(response.status_int, 302)
        self.assertRegexpMatches(response.headers['Location'], r'.*oauth2.*')

    @mock.patch.object(main.decorator, 'has_credentials', return_value=True)
    def test_oauthed_get(self, *args):
        self.loginUser()

        request = webapp2.Request.blank('/')

        mock_http = HttpMock(
            os.path.join(RESOURCE_PATH, 'datasets-list.json'),
            {'status': '200'})
        with mock.patch.object(main.decorator, 'http', return_value=mock_http):
            original_projectid = main.PROJECTID
            try:
                main.PROJECTID = self.constants['projectId']
                response = request.get_response(main.app)
            finally:
                main.PROJECTID = original_projectid

        # Should make the api call
        self.assertEqual(response.status_int, 200)
        self.assertRegexpMatches(
            response.body,
            re.compile(r'.*datasets.*datasetReference.*etag.*', re.DOTALL))
